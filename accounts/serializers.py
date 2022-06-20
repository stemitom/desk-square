from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from accounts.tokens import PasswordResetTokenGenerator, UserActivationTokenGenerator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("That email is not available")
        return email

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError("That username is not available")
        return username

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        data = {
            key: value
            for key, value in validated_data.items()
            if key
            not in (
                "password1",
                "password2",
            )
        }
        data["password"] = validated_data["password1"]
        user = self.Meta.model.objects.create_user(**data)
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "prefix",
            "phone",
            "job_title",
            "company",
            "website",
            "blog",
            "country",
            "postal_code",
            "is_email_verified",
            "email_verified_at",
        )


class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": "Token is invalid or expired"}

    def validate(self, data):
        self.token = data["refresh"]
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


class ActivateAccountSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        uid = data["uid"]
        token = data["token"]

        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (ObjectDoesNotExist, ValueError):
            raise serializers.ValidationError("Given user does not exist")

        activation_token = UserActivationTokenGenerator()
        if not activation_token.check_token(user, token):
            raise serializers.ValidationError("Given token is wrong")
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_pw = serializers.CharField(write_only=True, required=True)
    new_pw = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    new_pw_conf = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context["request"].user
        if not user.check_password(data["old_pw"]):
            raise serializers.ValidationError(
                "Password is incorrect. Please check and try again!"
            )
        if data["new_pw"] != data["new_pw_conf"]:
            raise serializers.ValidationError("Passwords must match")
        if data["new_pw"] == data["old_pw"]:
            raise serializers.ValidationError(
                "Old and New pasword cannot be the same. Please check and try again"
            )
        return data

    def save(self, **kwargs):
        password = self.validated_data["new_pw"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user


class ResetPasswordSerializer(serializers.Serializer):
    pass
