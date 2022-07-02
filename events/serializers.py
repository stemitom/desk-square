from rest_framework import serializers

from events.models import Event, Location, Media, Tag, Ticket, Attendee, TicketOrder
from timezone_field.rest_framework import TimeZoneSerializerField


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ("event",)


class TicketOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketOrder
        exclude = ("order_id",)


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        exclude = ("event",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class EventSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())
    tz = TimeZoneSerializerField(use_pytz=True)
    location = LocationSerializer()
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data.update({"creator": user})

        tags_data = validated_data.pop("tags")
        location_data = validated_data.pop("location")
        tickets_data = validated_data.pop("tickets")

        event = Event.objects.create(**validated_data)

        for tag in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag)
            event.tags.add(tag)

        ticket_instances = [Ticket(**data, event=event) for data in tickets_data]
        event.tickets.bulk_create(ticket_instances)

        Location.objects.create(event=event, **location_data)
        return event


class AttendeeSerializer(serializers.ModelSerializer):
    ticket_order = TicketOrderSerializer()

    class Meta:
        model = Attendee
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        event = self.context["event"].event
        quantity = request.query_params["ticket_qty"]

        user = request.user

        if user:
            validated_data.updated(
                {"name": user.name, "email": user.email, "user": attendee}
            )
        validated_data.updated({"event": event})

        attendee = Attendee.objects.create(**validated_data)
        TicketOrder.objects.create(
            user=attendee, tickets_purchased=event.ticket, quantity=quantity
        )
        return attendee
