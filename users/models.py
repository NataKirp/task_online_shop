from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='Аватар', blank=True, null=True,
                               help_text="Загрузите свой аватар")
    phone_number = PhoneNumberField(unique=True, verbose_name='Телефон', blank=True, null=True,
                                    help_text="Введите номер телефона")
    country = CountryField(verbose_name='Страна', blank=True, null=True, help_text='Выберите страну')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
