from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("That email is not available")
        return email

    def validate_username(self, username):
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError("That username is not available")
        return username

    def validate_password(self, password):
        password_minimum_length = 8
        if len(password) < password_minimum_length:
            raise serializers.ValidationError(
                f"Password minimum length allowed is {password_minimum_length}"
            )
        return password

    def create(self, validated_data):
        data = {
            key: value
            for key, value in validated_data.items()
            if key not in ("password",)
        }
        data["password"] = validated_data["password"]
        user = self.Meta.model.objects.create_user(**data)
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "prefix",
            "phone_number",
            "job_title",
            "company",
            "website",
            "blog",
            "country",
            "postal_code",
            "is_email_verified",
            "email_verified_at",
            "created_at",
            "updated_at",
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


class ChangePasswordSerializer(serializers.Serializer):
    old_pw = serializers.CharField(write_only=True, required=True)
    new_pw = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    new_pw_conf = serializers.CharField(write_only=True, required=True)

    def validate_old_pw(self, old_pw):
        user = self.context["request"].user
        if not user.check_password(old_pw):
            raise serializers.ValidationError(
                "Password is incorrect. Please check and try again!"
            )

    def validate(self, data):
        if data["new_pw"] != data["new_pw_conf"]:
            raise serializers.ValidationError("Passwords must match")
        if data["new_pw"] == data["old_pw"]:
            raise serializers.ValidationError(
                "Old and New password cannot be the same. Please check and try again"
            )
        return data

    def save(self, **kwargs):
        password = self.validated_data["new_pw"]
        user = self.context["request"].user
        user.set_password(password)
        user.save()
        return user
