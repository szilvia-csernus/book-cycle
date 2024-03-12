from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy_notice/', views.privacy_notice, name='privacy_notice'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('500/', views.error_500, name='error_500'),
    path('static-file-urls/', views.static_file_urls, name='static_file_urls'),
    path('serviceworker', views.serviceworker, name='serviceworker'),
]
