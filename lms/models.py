from django.conf import settings
from django.db import models


class Course(models.Model):

    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="courses/previews", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )

    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="lessons/previews", blank=True, null=True, verbose_name="Превью"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    video_url = models.URLField(max_length=200, verbose_name="Ссылка на видео")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return f"{self.title} ({self.course})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
