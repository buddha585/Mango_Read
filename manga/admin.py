from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Manga, Genre, Type, Comment


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ("id", "manga_name", "manga_type", "preview")
    fields = (
        "manga_name",
        "manga_type",
        "manga_genre",
        "manga_year",
        "manga_description",
        "preview",
        "manga_cover",
        "manga_slug",
    )
    list_display_links = ("manga_name",)
    search_fields = ("manga_name",)
    readonly_fields = ("preview",)
    prepopulated_fields = {"manga_slug": ("manga_name",)}

    def preview(self, obj):
        if obj.manga_cover:
            return mark_safe(
                f'<img src= "{obj.manga_cover.url}" width = "60" height = "60" />'
            )
        return "None"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "manga_genre")
    list_display_links = ("manga_genre",)
    search_fields = ("manga_genre",)


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id", "manga_type")
    list_display_links = ("manga_type",)
    search_fields = ("manga_type",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "manga",
    )
    list_display_links = ("manga",)
    search_fields = ("manga", "mango_read_user")