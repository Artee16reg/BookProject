from django.db import models


class Author(models.Model):
    """Афторы"""
    name = models.CharField("Имя", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class BookModel(models.Model):
    """Книги"""
    title = models.CharField("Название", max_length=250)
    description = models.TextField("Описание")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    author = models.ManyToManyField(Author, verbose_name="авторы")
    genre = models.ForeignKey(Genre, verbose_name="жанры", on_delete=models.CASCADE)
    image = models.ImageField("Изображение", upload_to="book_img/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    # метод позволяет выводить в админке М2М связь
    def author_names(self):
        return u" %s" % (u", ".join([author.name for author in self.author.all()]))

    author_names.short_description = u'Авторы'


class Chapter(models.Model):
    """Глава в книге"""
    title = models.CharField("Название", max_length=250)
    number = models.SmallIntegerField("Значение", default=0)
    text = models.TextField("Текст")
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Глава"
        verbose_name_plural = "Главы"
        ordering = ['number']

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    book = models.ForeignKey(
        BookModel,
        on_delete=models.CASCADE,
        verbose_name="книга",
        related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.book}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Comment(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True, related_name='children'
    )
    book = models.ForeignKey(BookModel, verbose_name="книга", on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"{self.name} - {self.book}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
