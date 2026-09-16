from django.db import models
from django.db.models import SET_NULL

from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Наименование',
        help_text='Введите наименование категории'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Введите описание категории'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('active', 'В продаже'),
        ('out_of_stock', 'Нет в наличии'),
        ('discontinued', 'Снят с продажи')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Наименование',
        help_text='Введите наименование продукта'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Введите описание продукта'
    )
    image = models.ImageField(
        upload_to='images/',
        blank=True,
        null=True,
        verbose_name='Изображение',
        help_text='Загрузите изображение продукта'
    )
    category = models.ForeignKey(
        Category,
        on_delete=SET_NULL,
        blank=True,
        null=True,
        related_name='products',
        help_text='Выберите категорию продукта'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за покупку',
        help_text='Введите цену'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец'
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', 'category']
        permissions = [
            ('can_unpublish_product', 'Может отменять публикацию продукта')
        ]

    # Переопределяем встроенный метод save
    def save(self, *args, **kwargs):
        # Если статус переключили на "Черновик", насильно гасим флаг публикации
        if self.status == 'draft':
            self.is_published = False

        # Если товар опубликован, но статус по ошибке остался черновиком — переводим в active
        elif self.is_published and self.status == 'draft':
            self.status = 'active'

        # Вызываем оригинальный метод сохранения Django, чтобы записать данные в базу
        super().save(*args, **kwargs)
