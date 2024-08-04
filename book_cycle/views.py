from django.shortcuts import render

def serviceworker(request):
    return render(request, 'serviceworker.js', content_type='application/javascript')
