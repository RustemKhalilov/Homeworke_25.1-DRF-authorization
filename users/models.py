from django.contrib.auth.models import AbstractUser
from django.db import models

from config.settings import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )

    city = models.CharField(
        max_length=150, verbose_name="Город", **NULLABLE, help_text="Укажите город"
    )

    phone = models.CharField(
        max_length=35, verbose_name="Телефон", **NULLABLE, help_text="Укажите телефон"
    )

    avatar = models.ImageField(
        upload_to="users/",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Выберите файл с " "аватаркой"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
