from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import FileExtensionValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import path_and_rename
from .managers import UserManager
class BaseModel(models.Model):
    objects = models.Manager()

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=100, unique=True, db_index=True, verbose_name="Имя", name="username"
    )
    nickname = models.CharField(max_length=60, verbose_name="Никнейм")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")
    is_superuser = models.BooleanField(default=False, verbose_name="Супер юзер")
    date_joined = models.DateField(auto_now_add=True, verbose_name="Дата регистраций")
    prof_pic = models.ImageField(
        upload_to=path_and_rename,
        blank=True,
        verbose_name="Фото профиля",
        default="user_images/default_user_image/default_user_image.jpeg",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpeg", "png", "jpg"]),
        ],
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "nickname",
    ]
    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    def __str__(self):
        return f"{self.username}, {self.nickname}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"