from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("registration", views.SignupView.as_view(), name="registration"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("list_users", views.ListUsersView.as_view(), name="list_users"),
]
