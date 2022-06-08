from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path(
        "registration",
        views.SignupView.as_view(),
        name="registration",
    ),
    path(
        "login",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "list_users",
        views.ListUsersView.as_view(),
        name="list_users",
    ),
    path(
        "request_activation",
        views.RequestActivationView.as_view(),
        name="request_activation",
    ),
    path(
        "activate",
        views.ActivateAccountView.as_view(),
        name="activate",
    ),
    path(
        "reset_pw",
        views.ChangePasswordView.as_view(),
        name="reset_password",
    ),
]
