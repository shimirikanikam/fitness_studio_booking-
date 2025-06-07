import pytz
import logging
from django.db import transaction
from django.utils.timezone import now, localtime
from rest_framework import status
from django.utils import timezone

from booking.models import FitnessClass, Booking
from helpers import message_codes
from helpers.custom_exceptions import BookingException

logger = logging.getLogger('api_logs')


def get_upcoming_classes(user_tz):
    upcoming_classes = FitnessClass.objects.filter(datetime__gte=now())

    class_data = [
        {
            "id": str(cls.id),
            "name": cls.name,
            "date_time": localtime(cls.datetime, user_tz).strftime
                ("%Y-%m-%d %H:%M:%S %Z"),
            "instructor": cls.instructor,
            "available_slots": cls.available_slots,
            "duration_minutes": cls.duration_minutes
        }
        for cls in upcoming_classes
    ]

    return {"class_data": class_data}

def create_booking(validated_data):
    class_id = validated_data['class_id']
    client_name = validated_data['client_name']
    client_email = validated_data['client_email']

    with transaction.atomic():
        try:
            fitness_class = FitnessClass.objects.get(id=class_id)
        except FitnessClass.DoesNotExist:
            logger.warning(f"Class not found: {class_id}")
            raise BookingException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=message_codes.UMI_4004_CLASS_NOT_FOUND_MESSAGE,
                message_code=message_codes.UMI_4004_CLASS_NOT_FOUND_CODE
            )

        if fitness_class.available_slots <= 0:
            logger.warning(f"No slots available for class {class_id}")
            raise BookingException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=message_codes.UMI_4005_NO_AVAILABLE_SLOTS_MESSAGE,
                message_code=message_codes.UMI_4005_NO_AVAILABLE_SLOTS_CODE
            )

        if Booking.objects.filter(fitness_class=fitness_class,
                                  client_email=client_email).exists():
            logger.error(f"Duplicate booking attempt: {client_email} for class {class_id}")
            raise BookingException(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=message_codes.UMI_4006_CLASS_ALREADY_BOOKED_MESSAGE,
                message_code=message_codes.UMI_4006_CLASS_ALREADY_BOOKED_CODE
            )

        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=client_name,
            client_email=client_email
        )

        fitness_class.available_slots -= 1
        fitness_class.save()

        ist = pytz.timezone('Asia/Kolkata')
        class_datetime_ist = fitness_class.datetime.astimezone(ist)

        return {
            'booking_id': str(booking.id),
            'class_id': str(fitness_class.id),
            'class_name': fitness_class.name,
            'instructor': fitness_class.instructor,
            'client_name': client_name,
            'client_email': client_email,
            'class_datetime': class_datetime_ist.strftime(
                "%Y-%m-%d %H:%M:%S %Z"),
            'remaining_slots': fitness_class.available_slots
        }

def get_user_bookings(validated_data):
    email_id = validated_data['email']

    bookings = Booking.objects.filter(
        client_email=email_id,
        is_cancelled=False
    ).select_related('fitness_class').order_by('-booking_time')

    if not bookings:
        raise BookingException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message_codes.UMI_4007_NO_BOOKINGS_FOUND_MESSAGE,
            message_code=message_codes.UMI_4007_NO_BOOKINGS_FOUND_CODE
        )

    booking_data = []
    for booking in bookings:
        booking_data.append({
            "booking_id": booking.id,
            "client_email": booking.client_email,
            "booking_time": booking.booking_time.strftime("%Y-%m-%d %H:%M:%S"),
            "class_name": booking.fitness_class.name,
            "class_time": booking.fitness_class.datetime.strftime(
                "%Y-%m-%d %H:%M:%S"),
            "instructor": booking.fitness_class.instructor,
            "class_duration": booking.fitness_class.duration_minutes
        })

    return {"bookings": booking_data}


def cancel_booking(booking_id):
    try:
        booking = Booking.objects.select_related('fitness_class').get(
            id=booking_id,
            is_cancelled=False
        )
    except Booking.DoesNotExist:
        raise BookingException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message_codes.UMI_4007_NO_BOOKINGS_FOUND_MESSAGE,
            message_code=message_codes.UMI_4007_NO_BOOKINGS_FOUND_CODE
        )

    # Check if class hasn't occurred yet
    if booking.fitness_class.datetime <= timezone.now():
        raise BookingException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message_codes.UMI_4008_CANNOT_CANCEL_PAST_CLASS_MESSAGE,
            message_code=message_codes.UMI_4008_CANNOT_CANCEL_PAST_CLASS_CODE
        )

    # Cancel the booking
    with transaction.atomic():
        booking.is_cancelled = True
        booking.cancelled_at = timezone.now()
        booking.save(update_fields=['is_cancelled', 'cancelled_at'])

        booking.fitness_class.available_slots += 1
        booking.fitness_class.save(update_fields=['available_slots'])
