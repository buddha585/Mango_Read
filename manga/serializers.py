from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Manga, Type, Comment, Genre
from users.models import User


class AuthorCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "nickname", "prof_pic")
        extra_kwargs = {
            "username": {"read_only": True},
            "nickname": {"read_only": True},
            "avatar": {"read_only": True},
        }


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class MangaSerializer(serializers.ModelSerializer):
    manga_genre = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all(), write_only=True
    )
    manga_slug = serializers.HiddenField(
        default="", validators=[UniqueValidator(queryset=Manga.objects.all())]
    )
    manga_name = serializers.CharField(
        max_length=65,
        min_length=4,
        validators=[UniqueValidator(queryset=Manga.objects.all())],
    )
    manga_cover = serializers.ImageField(default="")

    class Meta:
        model = Manga
        exclude = ("cover_width", "cover_height")
        extra_kwargs = {
            "manga_type": {"write_only": True},
            "manga_description": {"write_only": True},
        }


class CommentSerializer(serializers.ModelSerializer):
    manga = serializers.SerializerMethodField(
        default=serializers.CharField(read_only=True)
    )
    manga_user = AuthorCommentSerializer(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    comment = serializers.CharField(max_length=100, min_length=1, required=False)
    mango_id = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

        extra_kwargs = {
            "mango_read_user_id": {"read_only": True},
        }

    def get_manga(self, instance):
        return instance.manga.manga_name

    def get_mango_read_user(self, instance):
        return f"{instance.user.username}, {instance.user.nickname}"


class MangoDetailSerializer(serializers.ModelSerializer):
    mango_type = serializers.CharField(
        source="mango_type.type",
    )
    mango_genre = GenreSerializer(many=True)
    mango_comment = CommentSerializer(many=True)
    mango_slug = serializers.HiddenField(default="")

    class Meta:
        model = Manga
        exclude = ("cover_width", "cover_height")