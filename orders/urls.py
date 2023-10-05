from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('check_stock_and_update_bag/',
         views.check_stock_and_update_bag,
         name='check_stock_and_update_bag'),
    path('update_stock/<order_number>', views.update_stock,
         name='update_stock'),
    path('attach_user_profile_to_order/<order_number>',
         views.attach_user_profile_to_order,
         name='attach_user_profile_to_order'),
    path('checkout_success/<order_number>', views.checkout_success,
         name='checkout_success'),
    path('cache_checkout_data/', views.cache_checkout_data,
         name='cache_checkout_data'),
    path('orders_post/', views.orders_post, name='orders_post'),
    path('orders_pickup/', views.orders_pickup, name='orders_pickup'),
    path('orders_completed/', views.orders_completed, name='orders_completed'),
    path('order/<order_number>', views.order, name='order'),
    path('ship_item/<order_number>', views.ship_item, name='ship_item'),
]
