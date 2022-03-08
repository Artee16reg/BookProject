from rest_framework.response import Response
from rest_framework.views import APIView
from book import models
from .serializers import BookListSerializers, BookDetailSerializers, CommentCreateSerializers


class BookListView(APIView):
    """Список книг"""

    def get(self, request):
        books = models.BookModel.objects.all()
        serializer = BookListSerializers(instance=books, many=True)
        return Response(serializer.data)


class BookDetailView(APIView):
    """Вывод книги"""

    def get(self, request, pk):
        book = models.BookModel.objects.get(id=pk)
        serializer = BookDetailSerializers(instance=book)
        return Response(serializer.data)


class CommentCreateView(APIView):
    """Добавление Комментариев"""

    def post(self, request):
        comment = CommentCreateSerializers(data=request.data)
        if comment.is_valid():
            comment.save()
        else:
            print("хуйня какаято ")
        return Response(status=201)
