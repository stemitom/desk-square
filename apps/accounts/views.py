from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.accounts.serializers import (
    ChangePasswordSerializer,
    LogInSerializer,
    RefreshTokenSerializer,
    UserSerializer,
)
from apps.accounts.tasks import (
    send_async_account_activation_mail,
    send_async_password_reset_mail,
)
from apps.accounts.utils import verify_uid_and_token


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.exclude(email=self.request.user.email)


class DetailUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.all()


class CurrentUserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()

    def perform_create(self, serializer):
        user = serializer.save()
        send_async_account_activation_mail(user.pk, self.request)


class LoginView(TokenObtainPairView):
    serializer_class = LogInSerializer

    def get_object(self):
        return self.request.user


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestActivationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        send_async_account_activation_mail(self.request.user.pk, self.request)

        return Response(
            {
                "message": "Email verification sent to email! Check your email and use the link to verify your account"
            },
            status=status.HTTP_200_OK,
        )


class ActivateAccountView(GenericAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, *args, **kwargs):
        user, is_valid = verify_uid_and_token(**kwargs, token_type="activation")
        if is_valid:
            if user.is_email_verified:
                return Response(
                    {"message": "Account has already been activated!"},
                    status=status.HTTP_409_CONFLICT,
                )
            user.is_email_verified = True
            user.email_verified_at = timezone.now()
            user.save()

            return Response(
                {"message": "Your account has been activated successfully!"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "The token has expired, already used or invalid!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data, context={"request": self.request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, *args, **kwargs):
        data = self.request.data
        email = data.get("email")
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        if user:
            send_async_password_reset_mail(user.pk, self.request)
        return Response(
            {"message": "Please do check your email for further instructions!"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    pass
