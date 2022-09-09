from rest_framework import serializers
from timezone_field.rest_framework import TimeZoneSerializerField

from apps.events.models import Attendee, Event, Location, Tag, Ticket, TicketOrder


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
    ticket_orders = TicketOrderSerializer(read_only=True, many=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Attendee
        fields = "__all__"
        # exclude = ("event",)

    def create(self, validated_data):
        request = self.context["request"]
        event = self.context["event"]
        quantity = request.query_params["ticket_qty"]

        user = request.user

        if user:
            validated_data.update(
                {"name": user.get_full_name(), "email": user.email, "user": user}
            )
        validated_data.update({"event": event})
        if Attendee.objects.filter(**validated_data).exists():
            raise serializers.ValidationError(
                """You are already registered to this event!
                Please do check your email for registration and ticket details or contact support"""
            )
        attendee = Attendee.objects.create(**validated_data)
        ticket = Ticket.objects.filter(event=event).first()
        TicketOrder.objects.create(
            user=attendee, tickets_purchased=ticket, quantity=quantity
        )
        return attendee
