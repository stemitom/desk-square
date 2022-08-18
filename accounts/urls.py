from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("profile", views.CurrentUserView.as_view(), name="profile"),
    path(
        "list-users",
        views.ListUsersView.as_view(),
        name="list-users",
    ),
    path(
        "signup",
        views.SignupView.as_view(),
        name="signup",
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
        "request-activation",
        views.RequestActivationView.as_view(),
        name="request-activation",
    ),
    path(
        "activate/<str:uid>/<str:token>",
        views.ActivateAccountView.as_view(),
        name="activate",
    ),
    path(
        "change-password",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "request-password-reset",
        views.RequestPasswordResetView.as_view(),
        name="request-password-reset",
    ),
    path("<pk>", views.DetailUserView.as_view(), name="user"),
]
