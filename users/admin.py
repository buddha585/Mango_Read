from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "nickname", "preview")
    fields = (
        "username",
        "nickname",
        "prof_pic",
        "is_staff",
        "is_superuser",
        "is_active",
        "password",
        "preview",
    )
    list_display_links = ("username",)
    search_fields = ("username",)

    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.prof_pic:
            return mark_safe(
                f"<img src= '{obj.prof_pic.url}' style='max-height:100pk;' />"
            )
        return "None"