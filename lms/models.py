from django.db import models
from config.settings import NULLABLE


class Course(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="название курса",
        help_text="введите название курса",
    )
    preview = models.ImageField(
        upload_to="media/course_preview/",
        verbose_name="превью курса",
        **NULLABLE
    )
    description = models.TextField(
        verbose_name="описание курса",
        **NULLABLE,
        help_text="введите описание курса",
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="владелец курса",
        **NULLABLE
    )

    created_at = models.DateTimeField(
        **NULLABLE,
        verbose_name="Дата создания",
        help_text="Укажите дату создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        **NULLABLE,
        verbose_name="Дата изменения",
        help_text="Укажите дату изменения",
        auto_now=True,
    )

    def __str__(self):
        return f"{self.name}: {self.description}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name="название урока")
    lesson_description = models.TextField(
        verbose_name="описание урока", **NULLABLE
    )
    lesson_preview = models.ImageField(
        upload_to="media/lesson_preview",
        verbose_name="изображение урока",
        **NULLABLE,
    )
    lesson_url = models.CharField(
        max_length=300, verbose_name="ссылка на видео", **NULLABLE
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс", **NULLABLE
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="владелец урока",
        **NULLABLE,
    )

    def __str__(self):
        return f"{self.course}: {self.lesson_name} - {self.lesson_description}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
