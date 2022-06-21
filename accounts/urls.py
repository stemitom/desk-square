from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("me", views.CurrentUserView.as_view(), name="logged_in_user_details"),
    path(
        "list_users",
        views.ListUsersView.as_view(),
        name="list_users",
    ),
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
        "change_password",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "request_password_reset",
        views.RequestPasswordResetView.as_view(),
        name="request_password_reset",
    ),
]
