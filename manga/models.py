from django.db import models
from django.core.validators import FileExtensionValidator

from .utils import path_and_rename_cover

from pytils import translit


class Genre(models.Model):
    manga_genre = models.CharField(
        max_length=50, blank=True, unique=True, verbose_name="Жанр"
    )

    def __str__(self):
        return f"{self.manga_genre}"

    class Meta:
        ordering = ("id", "manga_genre")
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Type(models.Model):
    manga_type = models.CharField(
        max_length=20, blank=True, verbose_name="Тип"
    )

    def __str__(self):
        return f"{self.manga_type}"

    class Meta:
        ordering = ("id", "manga_type")
        verbose_name = "Тип"
        verbose_name_plural = "Типы"


class Manga(models.Model):
    manga_name = models.CharField(
        max_length=30,
        unique=True,
        name="manga_name",
        verbose_name="Название манги",
        db_index=True,
    )
    manga_genre = models.ManyToManyField(
        Genre, verbose_name="Жанр"
    )
    manga_type = models.ForeignKey(
        Type, on_delete=models.CASCADE, verbose_name="Тип"
    )
    release_year = models.DateField(verbose_name="Год релиза", null=True, blank=True)
    manga_year = models.DateField(verbose_name="Год", null=True, blank=True)
    manga_slug = models.SlugField(
        unique=True, db_index=True, verbose_name="URL", default=""
    )
    cover_height = models.IntegerField(default="1200")
    cover_width = models.IntegerField(default="800")
    manga_cover = models.ImageField(
        upload_to=path_and_rename_cover,
        blank=True,
        default="",
        null=True,
        width_field="cover_width",
        height_field="cover_height",
        verbose_name="Обложка манги",
        validators=(FileExtensionValidator(allowed_extensions=["png", "jpeg", "img"]),),
    )
    manga_description = models.TextField(max_length=280, verbose_name="Краткое описание")

    def save(self, *args, **kwargs):
        self.mango_slug = translit.slugify(self.manga_name)
        super(Manga, self).save(*args, **kwargs)

    def __str__(self):
        return self.manga_name

    class Meta:
        ordering = ("manga_slug",)
        verbose_name = "Манга"
        verbose_name_plural = "Манга"


class Comment(models.Model):
    mango_read_user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="manga_read_user"
    )
    manga = models.ForeignKey(
        Manga, on_delete=models.CASCADE, related_name="mango_read_comment"
    )
    comment = models.TextField(
        max_length=300, blank=True, verbose_name="Коментарий", name="comment"
    )

    def __str__(self):
        return f"{self.mango_read_user.prof_pic}{self.mango_read_user.username}"

    class Meta:
        verbose_name = "Коментарий"
        verbose_name_plural = "Коментарии"