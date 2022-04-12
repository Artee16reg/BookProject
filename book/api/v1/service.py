from django_filters import rest_framework as filters
from book.models import BookModel


def get_client_ip(request):
    """Получение IP пользоваеля"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
#     pass


class BookFilter(filters.FilterSet):
    """Филтер по авторам, дате, жанрам"""
    #author = CharFilterInFilter(field_name='author__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = BookModel
        fields = ['author__name', 'year', 'genre__name']
