from rest_framework import generics, permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Location, Media, Tag, Ticket
from .serializers import EventSerializer


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
