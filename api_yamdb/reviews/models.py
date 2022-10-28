from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from django.db import models

from reviews.utilites import current_year
from users.models import User


class AbstractModelGenreCategory(models.Model):
    name = models.CharField('Имя', max_length=settings.LIMIT_CHAT)
    slug = models.SlugField(
        'Slug', unique=True, max_length=settings.LIMIT_SLUG)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class AbstractModelReviewComment(models.Model):
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[settings.LIMIT_TEXT]


class Category(AbstractModelGenreCategory):
    class Meta(AbstractModelGenreCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        default_related_name = "categories"


class Genre(AbstractModelGenreCategory):
    class Meta(AbstractModelGenreCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        default_related_name = "genres"


class Title(models.Model):
    name = models.CharField(
        'Название произведения', max_length=settings.LIMIT_CHAT)
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        db_index=True,
        validators=[MinValueValidator(
                    limit_value=settings.MIN_LIMIT_VALUE,
                    message="Год не может быть меньше или равен нулю"),
                    MaxValueValidator(
                    limit_value=current_year,
                    message="Год не может быть больше текущего")])
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)
        default_related_name = "titles"


class AbstractModelReviewComments(models.Model):
    """Абстрактная модель для Review и Comments."""
    text = models.CharField(max_length=settings.LIMIT_CHAT)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def __str__(self):
        return self.text[settings.LIMIT_TEXT]

    class Meta:
        abstract = True
        ordering = ('pub_date',)


class Review(AbstractModelReviewComments):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        'Оценка',
        default=settings.MIN_LIMIT_VALUE,
        validators=[
            MinValueValidator(limit_value=settings.MIN_LIMIT_VALUE,
                              message='Минимальное значение рейтинга - 1'),
            MaxValueValidator(limit_value=settings.MAX_LIMIT_VALUE,
                              message='Максимальное значение рейтинга - 10')
        ],
    )

    class Meta(AbstractModelReviewComment.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]


class Comments(AbstractModelReviewComments):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta(AbstractModelReviewComments.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = "comments"
