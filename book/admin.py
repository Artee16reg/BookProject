from django.contrib import admin
from .models import *


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    readonly_fields = ("name", "email")


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 1


@admin.register(BookModel)
class BookModelAdmin(admin.ModelAdmin):
    # list_display = ('title', 'description', 'year', 'genre', 'author_names')
    list_filter = ('year', 'genre')
    search_fields = ('title', 'genre__name')
    inlines = [CommentInline, ChapterInline]
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': (('title', 'description'),)
        }),
        (None, {
            'fields': (('author', 'year', 'genre'),)
        })
    )


@admin.register(Comment)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы  к книге """
    list_display = ("name", "email", "parent", "book")  # id
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "book", "ip")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'book')
    search_fields = ('book',)
    list_filter = ('book',)


admin.site.register(Author)
admin.site.register(RatingStar)
