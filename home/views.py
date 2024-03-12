from django.views.static import serve
from django.shortcuts import render
from orders.context import manage_orders_details
from django.templatetags.static import static
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, JsonResponse


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


# Serve the service worker file from the same domain (not directly from S3) to
# have it in the same scope as the main page for the PWA manifest to work
def serviceworker(request):
    path = 'serviceworker.js'
    return serve(request, path, document_root=settings.STATICFILES_DIRS[0])


def static_file_urls(request):
    static_files = [
        '/css/account.css',
        '/css/base.css',
        '/css/checkout.css',
        '/css/home.css',
        '/css/inventory.css',
        '/css/loader.css',
        '/css/modal.css',
        '/css/orders.css',
        '/css/shopping_bag.css',
        '/js/bag.js',
        '/js/book_management.js',
        '/js/books.js',
        '/js/checkout.js',
        '/js/menu.js',
        '/js/modal.js',
        '/js/stripe_elements.js',
        '/js/toast.js',
    ]

    # Convert static file paths to absolute URLs
    static_file_urls = [request.build_absolute_uri(
        static(file)) for file in static_files]

    return JsonResponse(static_file_urls, safe=False)
