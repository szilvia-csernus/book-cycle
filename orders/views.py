from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderFormPost


def checkout(request):
    """ A view to return the checkout page """

    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There are no items in your bag yet")
        return redirect(reverse('books'))

    order_form = OrderFormPost()
    template = 'orders/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_5',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
