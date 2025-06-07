from django.urls import path

from booking.views import ClassListView, BookingCreateView, BookingListView, \
    BookingCancelView

urlpatterns = [
    path("class-list/", ClassListView.as_view(), name="class_list"),
    path("book/", BookingCreateView.as_view(), name="book_class"),
    path("bookings/", BookingListView.as_view(), name="booking_list"),
    path("cancel-booking/", BookingCancelView.as_view(), name="cancel_booking")
]
