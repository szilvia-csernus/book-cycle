from decimal import Decimal

from django.shortcuts import (render, redirect, reverse, get_object_or_404,
                              HttpResponse)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order
from inventory.models import Stock
from shopping_bag.context import bag_contents
from shopping_bag.views import update_bag
from profiles.models import UserProfile
from profiles.forms import UserProfileForm

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    Cache the checkout data in order to modify the payment intent.
    This only can be done on the backend, hence the need for this view.
    """
    try:
        post_data = json.loads(request.body.decode("utf-8"))
        print(post_data)
        pid = post_data['client_secret'].split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Add user's bag, save_info and user email to the
        # payment intent's metadata.
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': post_data['save_info'],
            'shipping_required': post_data['shipping_required'],
            # 'user_email': request.user.email,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """ A view to return the checkout page """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There are no items in your bag.")
        return redirect(reverse('books'))

    if request.method == 'POST':

        shipping_info = request.POST['shipping-info']

        if shipping_info == 'post':
            form_data = {
                'full_name': request.POST['full_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
                'town_or_city': request.POST['town_or_city'],
                'street_address1': request.POST['street_address1'],
                'street_address2': request.POST['street_address2'],
                'county': request.POST['county'],
            }
        else:
            form_data = {
                'full_name': request.POST['full_name'],
                'email': request.POST['email'],
                'phone_number': request.POST['phone_number'],
                'country': request.POST['country'],
                'postcode': request.POST['postcode'],
            }

        # print(form_data)

        order_form = OrderForm(form_data)
        if order_form.is_valid():

            # For optimazation, we prevent the first 'save' of the order from
            # being committed to the database until we have added the extra
            # info to the order. This is done by setting commit=False
            order = order_form.save(commit=False)
            if shipping_info == 'post':
                order.shipping_required = True
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item in bag.items():
                stock_item = Stock.objects.get(id=item[0])
                try:
                    order_line_item = OrderLineItem(
                        order=order,
                        stock_item=stock_item,
                        quantity=item[1],
                    )
                    order_line_item.save()
                except Stock.DoesNotExist:
                    # This scenario would only happen if an admin deleted a
                    # stock item from the database after a user added it to
                    # their bag. This should never happen, as there are
                    # other checks in place to prevent this from happening.
                    messages.error(request, (
                        "One or more of the textbooks in your bag were not "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save all the info to the user's session profile
            request.session['save_info'] = 'save-info' in request.POST

            return redirect(reverse('update_stock',
                                    args=[order.order_number]))
        else:
            # This scenario would not happen if the user is using the
            # front-end form, as the form would be validated before
            # the user is allowed to submit the form.
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
            return redirect(reverse('checkout'))
    else:
        # (GET request)
        current_bag = bag_contents(request)
        total = current_bag['total']

        # update grand total to include shipping cost
        shipping_required = False
        if 'shipping-info' in request.GET:
            shipping = request.GET['shipping-info']
            if shipping == 'post':
                shipping_required = True
        else:
            shipping_required = request.session.get('shipping_required', False)

        if shipping_required:
            total = total + Decimal(settings.SHIPPING_COST)

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        template = 'orders/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'shipping_required': shipping_required,
        }

        return render(request, template, context)


def check_stock_and_update_bag(request):
    """
    Check stock and update bag before checkout
    """
    bag = request.session.get('bag', {})
    books_removed_from_bag = 0
    for item in bag.items():
        try:
            stock_item = Stock.objects.get(id=item[0])
            difference = stock_item.quantity - item[1]
            if difference < 0:
                # Call the update_bag function with the quantity to remove
                quantity = (difference * -1)
                update_bag(request, stock_item.id, quantity_to_remove=quantity,
                           redirect_url=request.path)
                books_removed_from_bag = books_removed_from_bag + quantity

        except Stock.DoesNotExist:
            messages.warning(request, (
                "One or more of the textbooks in your order were not \
                found in our database, we had to remove it from your bag.\n\
                Apologies for the inconvenience!\n\
                Please review your bag before proceeding to checkout."))

        if books_removed_from_bag > 0:
            messages.warning(request, (
                f"One or more of the textbooks in your order were not \
                available in the quantity you requested. \
                We have removed {books_removed_from_bag} \
                book(s) from your bag.\n\
                Apologies for the inconvenience! \n\
                Please review your bag before proceeding to checkout."))

            return redirect(reverse('view_bag'))

    if 'shipping-info' in request.GET:
        shipping = request.GET['shipping-info']
        request.session['shipping_required'] = True if shipping == 'post' \
            else False

    return redirect(reverse('checkout'))


def update_stock(request, order_number):
    """
    Update stock when order is completed
    """
    order = get_object_or_404(Order, order_number=order_number)
    try:
        for item in order.lineitems.all():
            try:
                stock_item = item.stock_item
                stock_item.reduce_stock(item.quantity)
                stock_item.save()
            except ValueError:
                # Log this error to the shop owner's issue tracker
                messages.error(request, (
                    "One or more of the textbooks in your order were not "
                    "found in our database, please call us for assistance!"))

    except Stock.DoesNotExist:
        # Log this error to the shop owner's issue tracker
        messages.error(request, (
            "One or more of the textbooks in your order were not "
            "found in our database, please call us for assistance!"))

    return redirect(reverse('attach_user_profile_to_order',
                            args=[order.order_number]))


def attach_user_profile_to_order(request, order_number):
    """
    Attach the user's profile to the order
    """
    order = get_object_or_404(Order, order_number=order_number)
    save_info = request.session.get('save_info')

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        if save_info:
            # Save the user's info
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! A confirmation\
    email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    return redirect(reverse('checkout_success',
                            args=[order.order_number]))


def checkout_success(request, order_number):
    """
    Display success page after checkout
    """
    order = get_object_or_404(Order, order_number=order_number)

    template = 'orders/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
