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


class YearGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name'
    )


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name'
    )


admin.site.register(YearGroup, YearGroupAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Stock, StockAdmin)
