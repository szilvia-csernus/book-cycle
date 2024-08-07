from django.shortcuts import render
from orders.context import manage_orders_details
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponse, HttpResponseServerError, JsonResponse


def home(request):
    """ A view to return the home page """
    orders_details = manage_orders_details(request)
    context = {
        'orders_to_post_count': orders_details['orders_to_post_count'],
        'orders_to_collect_count': orders_details['orders_to_collect_count'],
    }
    return render(request, 'home/home.html', context)


def robots_txt(request):
    """ A view to return the robots.txt page - used for SEO """
    
    return render(request, 'home/robots.txt', content_type='text/plain')


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


def static_file_urls(request):
    static_files = [
        'css/account.css',
        'css/base.css',
        'css/checkout.css',
        'css/home.css',
        'css/inventory.css',
        'css/loader.css',
        'css/modal.css',
        'css/orders.css',
        'css/shopping_bag.css',
        'js/bag.js',
        'js/book_management.js',
        'js/books.js',
        'js/checkout.js',
        'js/menu.js',
        'js/modal.js',
        'js/stripe_elements.js',
        'js/toast.js',
    ]

    # Use staticfiles_storage for both development and production
    static_file_urls = [staticfiles_storage.url(file) for file in static_files]

    return JsonResponse(static_file_urls, safe=False)
