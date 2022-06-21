from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    LogInSerializer,
    RefreshTokenSerializer,
    ResetPasswordSerializer,
    UserSerializer,
)
from .utils import send_tokenified_email


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        User = get_user_model()
        return User.objects.exclude(email=self.request.user.email)


class CurrentUserView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


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


class RequestActivationView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args):
        send_tokenified_email(request.user, request, ctx="activation")
        return Response(
            {
                "message": "Email verification sent to email! Check your email and use the link to verify your account"
            },
            status=status.HTTP_200_OK,
        )


class ActivateAccountView(GenericAPIView):
    serializer_class = ActivateAccountSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user.is_email_verified:
            return Response(
                {"message": "Account has already been activated!"},
                status=status.HTTP_409,
            )
        user.is_email_verified = True
        user.save()

        return Response(
            {
                "message": "Email successfully verified! Your account is sucessfully activated!"
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, *args):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args):
        data = request.data
        try:
            email = data["email"]
            print(email)
        except KeyError:
            return Response(
                {"error": "Bad request"}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            User = get_user_model()
            user = User.objects.filter(email=email).first()
            if user:
                send_tokenified_email(user, request, ctx="passwordReset")
        return Response(
            {"message": "Please do check your email for further instructions!"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    pass
