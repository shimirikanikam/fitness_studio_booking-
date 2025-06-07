from django.db import models

class DefaultTimeStamp(models.Model):
    created_dtm = models.DateTimeField(auto_now_add=True)
    updated_dtm = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FitnessClass(DefaultTimeStamp):
    name = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    instructor = models.CharField(max_length=100)
    total_slots = models.PositiveIntegerField()
    available_slots = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=60)

    class Meta:
        db_table = "fitness_class"
        verbose_name = "Fitness Class"


class Booking(DefaultTimeStamp):
    fitness_class = models.ForeignKey(
        FitnessClass,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booking_time = models.DateTimeField(auto_now_add=True)
    is_cancelled = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "booking"
        verbose_name = "Booking"
