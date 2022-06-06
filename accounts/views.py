from django.contrib.auth import get_user_model

from rest_framework import status, generics, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    LogInSerializer,
    ActivateAccountSerializer,
    RefreshTokenSerializer,
)


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.exclude(email=self.request.user.email)


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


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


class ActivateAccountView(APIView):
    serializer_class = ActivateAccountSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args):
        serializer = ActivateAccountSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        user.is_email_verified = True
        user.save()

        return Response(
            {
                "message": "Email successfully verified! Your account is sucessfully activated!"
            },
            status=status.HTTP_200_OK,
        )


class PasswordChangeView:
    pass


class PasswordResetView:
    pass
