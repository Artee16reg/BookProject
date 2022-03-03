from django.contrib import admin
from .models import *


# @admin.register(BookModel)
# class AuthorAdmin(admin.ModelAdmin):
#
#     list_display = ('title', 'description', 'year', 'genres')
#     list_display_links = ('title',)
#     list_filter = ('year', 'genres')
#     search_fields = ('title', 'genres__name')


@admin.register(Comment)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы  к книге """
    list_display = ("name", "email", "parent", "book") # id
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "book", "ip")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


admin.site.register(Author)
admin.site.register(RatingStar)
admin.site.register(Chapter)
admin.site.register(BookModel)
