from django.db import models
from rest_framework import generics

from book.models import BookModel
from .serializers import BookListSerializers, BookDetailSerializers, CommentCreateSerializers, CreateRatingSerializer
from .service import get_client_ip


class BookListView(generics.ListAPIView):
    """Список книг"""
    serializer_class = BookListSerializers
    queryset = BookModel.objects.all()


class BookDetailView(generics.RetrieveAPIView):
    """Вывод книги"""

    serializer_class = BookDetailSerializers

    def get_queryset(self):  # TO DO
        book = BookModel.objects.filter().annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return book


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

