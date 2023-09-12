from django.shortcuts import render, redirect, get_object_or_404
from inventory.models import Stock


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

    stock_item.block_1_stock()

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def remove_from_bag(request, stock_id):
    """ Add one book to the shopping bag """

    stock_item = get_object_or_404(Stock, id=stock_id)
    bag = request.session.get('bag', {})
    redirect_url = request.POST.get('redirect_url')

    if stock_id in list(bag.keys()) and bag[stock_id] > 0:
        bag[stock_id] -= 1
    else:
        bag[stock_id] = 0

    stock_item.unblock_1_stock()

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
