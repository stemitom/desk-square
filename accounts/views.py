from django.contrib.auth import get_user_model

from rest_framework import status, generics, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, LogInSerializer, RefreshTokenSerializer


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


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.exclude(email=self.request.user.email)

    def list(self, request, *args, **kwargs):
        print(request.user.email)
        return super().list(request, *args, **kwargs)


class ActivateAccountView:
    pass


class PasswordChangeView:
    pass


class PasswordResetView:
    pass
