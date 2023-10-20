from django.shortcuts import render
from orders.context import manage_orders_details
from django.http import HttpResponse, HttpResponseServerError


def home(request):
    """ A view to return the home page """
    orders_details = manage_orders_details(request)
    context = {
        'orders_to_post_count': orders_details['orders_to_post_count'],
        'orders_to_collect_count': orders_details['orders_to_collect_count'],
    }
    return render(request, 'home/home.html', context)


def privacy_notice(request):
    """ A view to return the privacy notice page """
    return render(request, 'home/privacy_notice.html')


def sitemap(request):
    """ A view to return the sitemap page - used for SEO """
    with open('sitemap.xml', 'rb') as f:
        sitemap_content = f.read()

    response = HttpResponse(sitemap_content, content_type='application/xml')

    return response


def error_500(request):
    """ A view to return the 500 error page for testing purposes"""
    try:
        1 / 0
        return HttpResponse("Impossible Success")
    except Exception:
        raise HttpResponseServerError("Intentional 500 Error")
