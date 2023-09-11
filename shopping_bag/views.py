from django.shortcuts import render, redirect


def view_bag(request):
    """ A view to return the shopping bag page """

    return render(request, 'shopping_bag/bag.html')


def add_to_bag(request, stock_id):
    """ Add one book to the shopping bag """

    bag = request.session.get('bag', {})
    redirect_url = request.POST.get('redirect_url')

    if stock_id in list(bag.keys()):
        bag[stock_id] += 1
    else:
        bag[stock_id] = 1

    request.session['bag'] = bag
    return redirect(redirect_url)
