from django.db import models
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from book.models import BookModel, Chapter
from .serializers import BookListSerializers, BookDetailSerializers, \
    CommentCreateSerializers, CreateRatingSerializer, ReadBookSerializers
from .service import get_client_ip, BookFilter


class BookListView(generics.ListAPIView):  # TO DO maybe ViewSet?
    """Список книг"""
    serializer_class = BookListSerializers
    queryset = BookModel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter


class BookDetailView(generics.RetrieveAPIView):
    """Вывод книги"""

    serializer_class = BookDetailSerializers

    def get_queryset(self):
        book = BookModel.objects.filter().annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return book


class ReadingBook(generics.ListAPIView):
    """Чтение книги"""

    serializer_class = ReadBookSerializers

    def get_queryset(self):
        id_book = self.kwargs['pk']
        read_book = Chapter.objects.filter(book_id=id_book)
        return read_book


class CommentCreateView(generics.CreateAPIView):
    """Добавление Комментариев"""
    serializer_class = CommentCreateSerializers
    # def post(self, request):
    #     comment = CommentCreateSerializers(data=request.data)
    #     if comment.is_valid():
    #         comment.save()
    #     else:
    #         print("хуйня кOкOято ")
    #     return Response(status=201)


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
