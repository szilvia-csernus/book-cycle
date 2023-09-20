from decimal import Decimal

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderFormPost
from .models import OrderLineItem, Order
from inventory.models import Stock
from shopping_bag.context import bag_contents

import stripe


def checkout(request):
    """ A view to return the checkout page """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There are no items in your bag yet")
        return redirect(reverse('books'))

    if request.method == 'POST':
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

        order_form = OrderFormPost(form_data)
        if order_form.is_valid():

            # For optimazation, we prevent the first 'save' of the order from
            # being committed to the database until we have added the extra
            # info to the order. This is done by setting commit=False
            # order = order_form.save(commit=False)
            order = order_form.save()
            # pid = request.POST.get('client_secret').split('_secret')[0]
            # order.stripe_pid = pid
            # order.original_bag = json.dumps(bag)
            # order.save()
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
                    messages.error(request, (
                        "One or more of the textbooks in your bag were not "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:
        current_bag = bag_contents(request)
        total = current_bag['total']
        if 'shipping-info' in request.GET:
            shipping = request.GET['shipping-info']
            if shipping == 'post':
                total = total + Decimal(3.50)

        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        print(intent)

        order_form = OrderFormPost()
        template = 'orders/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    for item in order.lineitems.all():
        stock_item = item.stock_item
        stock_item.reduce_stock(item.quantity)
        stock_item.save()

    # if request.user.is_authenticated:
    #     profile = UserProfile.objects.get(user=request.user)
    #     # Attach the user's profile to the order
    #     order.user_profile = profile
    #     order.save()

    #     # Save the user's info
    #     if save_info:
    #         profile_data = {
    #             'default_phone_number': order.phone_number,
    #             'default_country': order.country,
    #             'default_postcode': order.postcode,
    #             'default_town_or_city': order.town_or_city,
    #             'default_street_address1': order.street_address1,
    #             'default_street_address2': order.street_address2,
    #             'default_county': order.county,
    #         }
    #         user_profile_form = UserProfileForm(profile_data, instance=profile)
    #         if user_profile_form.is_valid():
    #             user_profile_form.save()

    # messages.success(request, f'Order successfully processed! \
    #     Your order number is {order_number}. A confirmation \
    #     email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'orders/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
