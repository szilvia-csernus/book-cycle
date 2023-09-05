from django.contrib import admin
from .models import YearGroup, Subject, Book, Stock

# Register your models here.
admin.site.register(YearGroup)
admin.site.register(Subject)
admin.site.register(Book)
admin.site.register(Stock)
