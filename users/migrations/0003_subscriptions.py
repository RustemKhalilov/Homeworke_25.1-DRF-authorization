# Generated by Django 5.0.7 on 2024-08-24 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0002_initial"),
        ("users", "0002_payments"),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscriptions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата начала подписки"
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscribed_course",
                        to="lms.course",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriber",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "подписка",
                "verbose_name_plural": "подписки",
            },
        ),
    ]
