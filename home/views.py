from django.shortcuts import render


def home(request):
    """ A view to return the home page """
    return render(request, 'home/home.html')


def privacy_notice(request):
    """ A view to return the privacy notice page """
    return render(request, 'home/privacy_notice.html')
