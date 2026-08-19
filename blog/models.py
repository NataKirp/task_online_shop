from django.db import models
from django.db.models import PositiveIntegerField


class Article(models.Model):
    title = models.CharField(
        max_length=250,
        unique=True,
        verbose_name='Заголовок',
        help_text='Введите заголовок статьи'
    )
    content = models.TextField(
        verbose_name='Содержимое',
        help_text='Введите содержимое статьи'
    )
    preview = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликована'
    )
    publication_date = models.DateField(
        verbose_name='Дата публикации',
        blank=True,
        null=True
    )
    views_counter = PositiveIntegerField(
        verbose_name='Счетчик просмотров',
        default=0
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
