from django.contrib.auth import password_validation
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User

import re


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "nickname", "avatar")


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        help_text="Username should contain only alphabetical characters",
    )

    password = serializers.CharField(
        max_length=28,
        min_length=6,
        required=True,
        write_only=True,
        style={"input_type": "password"},
        validators=[password_validation.validate_password],
        help_text=password_validation.password_validators_help_texts(),
    )
    nickname = serializers.CharField(
        required=True,
        help_text="Nickname should contain only alphanumerical characters",
    )
    avatar = serializers.ImageField(
        default="https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg"
    )

    class Meta:
        model = User
        fields = ("username", "prof_pic", "nickname", "password")

    def validate(self, attrs):
        username = attrs.get("username", "")
        nickname = attrs.get("nickname", "")
        if re.findall("[#$%!^&*0-9]", username):
            raise ValidationError(
                "Username should contain only alphabetical characters"
            )
        if not str(nickname).isalnum():
            raise ValidationError(
                "Nickname should contain only alphanumerical characters"
            )
        if username == nickname:
            raise ValidationError("Username and Nickname cant be the same")

        return super(RegisterSerializer, self).validate(attrs)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            nickname=validated_data["nickname"],
            prof_pic=validated_data["prof_pic"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})
    tokens = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account is disabled, contact admin")
        return {
            "username": user.username,
            "tokens": user.tokens(),
        }