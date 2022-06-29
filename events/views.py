from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Location, Media, Tag, Ticket, Attendee
from .serializers import EventSerializer, AttendeeSerializer


class CreateEventView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors)


class RegisterForEventView(generics.CreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Attendee.objects.all()

    def create(self, request, *args, **kwargs):
        event_id = kwargs["event_id"]
        event = Event.objects.filter(id=kwargs["event_id"])
        if event:
            if request.user.is_authenticated and request.user.id == event.id:
                return Response(
                    {
                        "error": "You can't register for an event you created, please try again!"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

        else:
            return Response({"error": f"Event with ID {event_id} does not exist"})
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "event": event}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors)
