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
        bag[str(stock_id)] += 1
    else:
        bag[str(stock_id)] = 1
        messages.success(
            request, f'{stock_item.book.title} was added to your bag')

    stock_item.block_1_stock()

    request.session['bag'] = bag
    return redirect(redirect_url)


def remove_from_bag(request, stock_id, quantity_to_remove=1):
    """ POST request: Remove stock items from the shopping bag """

    redirect_url = request.POST.get('redirect_url')

    try:
        stock_item = Stock.objects.get(id=stock_id)
        bag = request.session.get('bag', {})

        if str(stock_id) in bag:

            quantity_to_remove = int(quantity_to_remove)
            if quantity_to_remove >= bag[str(stock_id)]:
                bag.pop(str(stock_id))
                messages.success(request, f'{stock_item.book.title}\
                                 (condition: {stock_item.condition}) was\
                                 removed from your bag')
            else:
                bag[str(stock_id)] = bag[str(stock_id)] - quantity_to_remove

            stock_item.unblock_stock(quantity_to_remove)

        request.session['bag'] = bag
        return redirect(redirect_url)

    except Stock.DoesNotExist:
        bag.pop(str(stock_id))

    except Exception as e:
        messages.error(
            request, f'Error removing stock: {stock_item.book.title}\
            \n Error: {e}')
        return HttpResponse(status=500)


def update_bag(request, stock_id, quantity_to_remove, redirect_url):
    """ GET request: Update shopping bag before checkout """

    try:
        stock_item = Stock.objects.get(id=stock_id)
        bag = request.session.get('bag', {})

        if str(stock_id) in bag:
            quantity_to_remove = int(quantity_to_remove)
            if quantity_to_remove >= bag[str(stock_id)]:
                bag.pop(str(stock_id))
            else:
                bag[str(stock_id)] = bag[str(stock_id)] - quantity_to_remove

        request.session['bag'] = bag
        return redirect(redirect_url)

    except Stock.DoesNotExist:
        bag.pop(str(stock_id))
        return redirect(redirect_url)

    except Exception as e:
        messages.error(
            request, f'Error removing stock: {stock_item.book.title}\
            \n Error: {e}')
        return HttpResponse(status=500)
