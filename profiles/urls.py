from django.urls import path
from .views import CustomSignupView
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('accounts/signup/', CustomSignupView.as_view(),
         name='account_signup'),
    path('order_history/<order_number>', views.order_history,
         name='order_history'),
]
