from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('privacy_notice/', views.privacy_notice, name='privacy_notice')
]
