from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from inventory.models import Stock
from profiles.models import UserProfile

import stripe
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customer_email = order.email
        subject = render_to_string(
            'orders/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'orders/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info
        shipping_required = intent.metadata.shipping_required
        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        email = billing_details.email

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    stripe_pid=pid,
                )
                order_exists = True
                break

            except Order.DoesNotExist:
                print('order does not exist')
                # if order is not found, the webhook will try again max 5 times
                # over 5 seconds before giving up and creating a new order
                attempt += 1
                time.sleep(1)

        if order_exists:
            print('order exists')
            self._send_confirmation_email(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Verified order already in database'),
                status=200)
        else:
            order = None
            try:
                order = Order.objects.create(
                    user_profile=profile,
                    full_name=billing_details.name,
                    email=billing_details.email,
                    phone_number=billing_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    shipping_required=shipping_required,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                if shipping_required:
                    order.town_or_city = shipping_details.address.city,
                    order.street_address1 = shipping_details.address.line1,
                    order.street_address2 = shipping_details.address.line2,
                    order.county = shipping_details.address.state,

                for item in json.loads(bag).items():
                    stock_item = Stock.objects.get(id=item[0])
                    order_line_item = OrderLineItem(
                        order=order,
                        stock=stock_item,
                        quantity=item[1],
                    )
                    order_line_item.save()

                if username != 'AnonymousUser':
                    profile = UserProfile.objects.get(user__email=email)
                    if save_info:
                        profile.default_phone_number = \
                            shipping_details.phone
                        profile.default_country = \
                            shipping_details.address.country
                        profile.default_postcode = \
                            shipping_details.address.postal_code
                        profile.default_town_or_city = \
                            shipping_details.address.city
                        profile.default_street_address1 =\
                            shipping_details.address.line1
                        profile.default_street_address2 =\
                            shipping_details.address.line2
                        profile.default_county = shipping_details.address.state
                        profile.save()

            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

            self._send_confirmation_email(order)
            return HttpResponse(
                content=(f'Webhook received: {event["type"]} | SUCCESS: '
                         'Created order in webhook'),
                status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        print('payment intent failed')
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
