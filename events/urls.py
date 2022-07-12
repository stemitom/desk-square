from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path(
        "",
        views.ListCreateEventView.as_view(),
        name="list_create_event",
    ),
    path(
        "<int:pk>",
        views.RetrieveUpdateDestroyEventView.as_view(),
        name="retrieve_update_destroy_event",
    ),
    path(
        "<int:event_id>/register",
        views.RegisterForEventView.as_view(),
        name="register_for_event_view",
    ),
    path(
        "search",
        views.SearchEventByTag.as_view(),
        name="search_event_by_tag",
    ),
    path(
        "me",
        views.ListAttendeeEvents.as_view(),
        name="list_all_attendee_events",
    ),
]
