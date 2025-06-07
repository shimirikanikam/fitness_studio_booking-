from rest_framework import serializers
from helpers.validators import validate_alphabetic_only


class BookingCreateSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    client_name = serializers.CharField(validators=[validate_alphabetic_only('name')], min_length=2)
    client_email = serializers.EmailField()


class BookingListSerializer(serializers.Serializer):
    email = serializers.EmailField()

class BookingSerializer(serializers.Serializer):
    booking_id = serializers.IntegerField()