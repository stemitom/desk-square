from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Attendee, Event, Tag
from .serializers import AttendeeSerializer, EventSerializer


class ListCreateEventView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors)


class RetrieveUpdateDestroyEventView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)


class RegisterForEventView(generics.CreateAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Attendee.objects.all()

    def create(self, request, *args, **kwargs):
        event_id = kwargs["event_id"]
        event = Event.objects.filter(id=kwargs["event_id"]).first()
        if event:
            if request.user.is_authenticated and request.user.id == event.creator.id:
                return Response(
                    {
                        "error": "You can't register for an event you created, please try again!"
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            return Response(
                {"error": f"Event with ID {event_id} does not exist"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = self.get_serializer(
            data=request.data, context={"request": request, "event": event}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors)


class SearchEventByTag(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Event.objects.all()

    def retrieve(self, request, *args, **kwargs):
        tag = request.query_params["tag"]
        tag = Tag.objects.filter(name=tag)
        event = Event.objects.filter(tags__in=tag)
        event_serializer = EventSerializer(event, many=True)
        return Response(data=event_serializer.data, status=status.HTTP_200_OK)


class ListAttendeeEvents(generics.ListAPIView):
    serializer_class = AttendeeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Attendee.objects.filter(user=self.request.user)
