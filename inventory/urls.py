from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.all_books, name='books'),
    path('book_detail/<slug:slug>/', views.book_detail, name='book_detail'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<slug:slug>/', views.edit_book, name='edit_book'),
    path('delete_book/<slug:slug>/', views.delete_book, name='delete_book'),
    path('manage_stock/<slug:slug>/', views.manage_stock, name='manage_stock'),
    path('add_stock//<stock_id>', views.add_stock, name='add_stock'),
    path('reduce_stock/<stock_id>', views.reduce_stock, name='reduce_stock'),
    path('book-image-urls/', views.book_image_urls, name='book_image_urls')
]
