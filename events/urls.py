from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path(
        "create",
        views.CreateEventView.as_view(),
        name="create_event",
    ),
    path(
        "<int: event_id>/register",
        views.RegisterForEventView,
        name="register_for_event_view",
    ),
]
