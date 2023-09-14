from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import Stock
from django.http import HttpResponse
from django.contrib import messages


def view_bag(request):
    """ A view to return the shopping bag page """

    return render(request, 'shopping_bag/bag.html')


def add_to_bag(request, stock_id):
    """ Add one book to the shopping bag """

    stock_item = get_object_or_404(Stock, id=stock_id)
    bag = request.session.get('bag', {})
    redirect_url = request.POST.get('redirect_url')

    if stock_id in list(bag.keys()):
        bag[stock_id] += 1
    else:
        bag[stock_id] = 1
    messages.success(request, f'{stock_item.book.title} was added to your bag')

    stock_item.block_1_stock()

    request.session['bag'] = bag
    return redirect(redirect_url)


def remove_from_bag(request, stock_id):
    """ Remove one book from the shopping bag """

    try:
        stock_item = get_object_or_404(Stock, id=stock_id)
        bag = request.session.get('bag', {})
        redirect_url = request.POST.get('redirect_url')

        if stock_id in list(bag.keys()) and bag[stock_id] > 1:
            bag[stock_id] -= 1

        if stock_id in list(bag.keys()) and bag[stock_id] == 1:
            bag.pop(stock_id)
            messages.warning(request, f'{stock_item.book.title}\
                             condition: {stock_item.condition} \
                             was removed from your bag')

        stock_item.unblock_1_stock()

        request.session['bag'] = bag
        return redirect(redirect_url)
    except Exception as e:
        messages.error(
            request, f'Error removing book: {stock_item.book.title} \
            \n Error: {e}')
        return HttpResponse(status=500)


def add_shipping(request):
    """ Add shipping info to context """

    request.session.get('bag', 0)
    req_shipping = request.POST.get('shipping_option')
    if req_shipping == 'True':
        request.session['shipping_option'] = True
    else:
        request.session['shipping_option'] = False

    redirect_url = request.POST.get('redirect_url')
    return redirect(redirect_url)
