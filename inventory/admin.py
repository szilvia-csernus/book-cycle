from django.contrib import admin
from .models import YearGroup, Subject, Book, Stock


class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'year_group',
        'subject',
        'exam_board',
        'publisher',
        'image'
    )

    ordering = ('year_group', 'subject')


class StockAdmin(admin.ModelAdmin):
    list_display = (
        'book',
        'condition',
        'price',
        'quantity'
    )


admin.site.register(YearGroup)
admin.site.register(Subject)
admin.site.register(Book, BookAdmin)
admin.site.register(Stock, StockAdmin)
