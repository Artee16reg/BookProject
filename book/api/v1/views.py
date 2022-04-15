from django.db import models
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from book.models import BookModel, Chapter, Comment
from book.api.v1 import serializers
from .service import get_client_ip, BookFilter


class BookListView(generics.ListAPIView):  # TODO may be ViewSet?
    """Список книг"""
    serializer_class = serializers.BookListSerializers
    queryset = BookModel.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = BookFilter
    search_fields = ['title']


class BookDetailView(generics.RetrieveAPIView):
    """Вывод книги"""

    serializer_class = serializers.BookDetailSerializers

    def get_queryset(self):
        book = BookModel.objects.filter().annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return book


class ChapterBookView(generics.ListAPIView):  # TODO you need add pagination
    """Чтение книги"""

    serializer_class = serializers.ChapterBookSerializers

    def get_queryset(self):
        id_book = self.kwargs['pk']
        read_book = Chapter.objects.filter(book_id=id_book)
        return read_book


class CommentCreateView(generics.CreateAPIView):  # TODO may be ViewSet?
    """Добавление Комментариев"""
    serializer_class = serializers.CommentCreateSerializers
    # def post(self, request):
    #     comment = CommentCreateSerializers(data=request.data)
    #     if comment.is_valid():
    #         comment.save()
    #     else:
    #         print("хуйня кOкOято ")
    #     return Response(status=201)


class CommentUpdateView(generics.UpdateAPIView):
    """Обновление Комментариев"""
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializers


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""

    serializer_class = serializers.CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
