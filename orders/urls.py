from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('check_stock_and_update_bag/<order_number>',
         views.check_stock_and_update_bag,
         name='check_stock_and_update_bag'),
    path('update_stock/<order_number>', views.update_stock,
         name='update_stock'),
    path('checkout_success/<order_number>', views.checkout_success,
         name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
]
