from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.all_books, name='books'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<slug:slug>/', views.edit_book, name='edit_book'),
    path('delete_book/<slug:slug>/', views.delete_book, name='delete_book')
]
