from rest_framework import serializers

from book.models import BookModel, Comment, Rating


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр комментариев, только parents"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class CommentCreateSerializers(serializers.ModelSerializer):
    """ Добавление Комментариев """

    class Meta:
        model = Comment
        fields = '__all__'


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсивно children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializers(serializers.ModelSerializer):
    """ Вывод комментарий """
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Comment
        fields = ('name', 'text', 'children')


class BookListSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    class Meta:
        model = BookModel
        fields = ('id', 'title', 'description', 'year', 'author', 'genre', 'image')


class BookDetailSerializers(serializers.ModelSerializer):
    """Список книг"""
    genre = serializers.SlugRelatedField(slug_field='name', read_only=True)
    rating_user = serializers.BooleanField()
    # genre = serializers.CharField(source='genre.name', max_length=250)
    middle_star = serializers.IntegerField()
    comments = CommentSerializers(many=True)

    class Meta:
        model = BookModel
        fields = ('id', 'title', 'description', 'year', 'author',
                  'genre', 'image', 'rating_user', 'middle_star', 'comments')
        depth = 4


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга пользователем"""

    class Meta:
        model = Rating
        fields = ("star", "book")

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            book=validated_data.get('book', None),
            defaults={'star': validated_data.get("star")}
        )
        return rating
