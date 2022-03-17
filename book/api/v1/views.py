from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import BookModel
from .serializers import BookListSerializers, BookDetailSerializers, CommentCreateSerializers, CreateRatingSerializer
from .service import get_client_ip


class BookListView(APIView):
    """Список книг"""

    def get(self, request):
        book = BookModel.objects.all()
        serializer = BookListSerializers(instance=book, many=True)
        return Response(serializer.data)



class BookDetailView(APIView):
    """Вывод книги"""

    def get(self, request, pk):
        books = BookModel.objects.filter(id=pk).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        serializer = BookDetailSerializers(instance=books, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView):
    """Добавление Комментариев"""

    def post(self, request):
        comment = CommentCreateSerializers(data=request.data)
        if comment.is_valid():
            comment.save()
        else:
            print("хуйня кOкOято ")
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
