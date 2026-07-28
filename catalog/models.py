from django.db import models
from django.db.models import SET_NULL


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Наименование',
                            help_text='Введите наименование категории')
    description = models.TextField(blank=True, null=True, verbose_name='Описание',
                                   help_text='Введите описание категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Наименование',
                            help_text='Введите наименование продукта')
    description = models.TextField(blank=True, null=True, verbose_name='Описание',
                                   help_text='Введите описание продукта')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Изображение',
                              help_text='Загрузите изображение продукта')
    category = models.ForeignKey(Category, on_delete=SET_NULL, blank=True, null=True, related_name='products',
                                 help_text='Выберите категорию продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за покупку',
                                help_text='Введите цену')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', 'category']
