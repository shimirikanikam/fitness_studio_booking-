from json import JSONDecodeError
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.views import APIView
import logging
import pytz
from booking.serializers import BookingCreateSerializer, BookingListSerializer, \
    BookingSerializer
from helpers import message_codes
from helpers.booking_helper import get_upcoming_classes, create_booking, \
    get_user_bookings, cancel_booking
from helpers.custom_exceptions import BookingException
from helpers.generic_response_utils import log_and_respond, \
    format_serializer_errors

logger = logging.getLogger('api_logs')


# Create your views here.
class ClassListView(APIView):

    def get(self, request):
        exception = response_data = None
        try:
            user_timezone = request.GET.get('timezone', 'Asia/Kolkata')

            try:
                user_tz = pytz.timezone(user_timezone)
            except pytz.UnknownTimeZoneError:
                logger.error(f"Invalid timezone provided: {user_timezone}")
                return log_and_respond(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=message_codes.UMI_4001_INVALID_TIMEZONE_MESSAGE,
                    message_code=message_codes.UMI_4001_INVALID_TIMEZONE_CODE
                )

            logger.info(f"Fetching upcoming classes for timezone: {user_timezone}")
            response_data = get_upcoming_classes(user_tz)

            status_code = status.HTTP_200_OK
            message = message_codes.UMI_2000_DATA_RETRIEVAL_SUCCESS_MESSAGE
            message_code = message_codes.UMI_2000_DATA_RETRIEVAL_SUCCESS_CODE

        except Exception as ex:
            logger.error(f"Unexpected error occurred while retrieving class data {str(ex)}", exc_info=True)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_MESSAGE
            message_code = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_CODE
            exception = ex

        return log_and_respond(
            data=response_data,
            status=status_code,
            message=message,
            message_code=message_code,
            exception=exception
        )


class BookingCreateView(APIView):
    def post(self, request):
        exception = response_data = None
        try:
            serializer = BookingCreateSerializer(data=request.data)

            if not serializer.is_valid():
                logger.error(f"Invalid booking data: {serializer.errors}")
                return log_and_respond(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=message_codes.UMI_4002_INVALID_REQUEST_BODY_MESSAGE,
                    message_code=message_codes.UMI_4002_INVALID_REQUEST_BODY_CODE,
                    error_info = format_serializer_errors(serializer.errors)
                )

            response_data = create_booking(serializer.validated_data)
            logger.info(f"Booking created successfully: {response_data.get('booking_id')}")

            status_code = status.HTTP_200_OK
            message = message_codes.UMI_2000_CLASS_BOOKING_SUCCESS_MESSAGE
            message_code = message_codes.UMI_2000_CLASS_BOOKING_SUCCESS_CODE

        except (ParseError, JSONDecodeError) as ex:
            logger.error(f"JSON parsing error occurred while creating booking for a client: {str(ex)}")
            status_code = status.HTTP_400_BAD_REQUEST
            message = message_codes.UMI_4002_INVALID_REQUEST_BODY_MESSAGE
            message_code = message_codes.UMI_4002_INVALID_REQUEST_BODY_CODE
            exception = ex

        except BookingException as ex:
            logger.error(f"Booking error in BookingCreateView: {ex.message} (code: {ex.message_code})")
            status_code = ex.status_code
            message = ex.message
            message_code = ex.message_code
            exception = ex

        except Exception as ex:
            logger.error(f"Unexpected error in BookingCreateView: {str(ex)}", exc_info=True)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_MESSAGE
            message_code = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_CODE
            exception = ex

        return log_and_respond(
            data=response_data,
            status=status_code,
            message=message,
            message_code=message_code,
            exception=exception
        )


class BookingListView(APIView):
    def get(self, request):
        exception = response_data = None
        try:
            serializer = BookingListSerializer(data=request.GET)

            if not serializer.is_valid():
                logger.error(f"Invalid request parameters: {serializer.errors}")
                return log_and_respond(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=message_codes.UMI_4002_INVALID_REQUEST_BODY_MESSAGE,
                    message_code=message_codes.UMI_4002_INVALID_REQUEST_BODY_CODE,
                    error_info=format_serializer_errors(serializer.errors)
                )

            response_data = get_user_bookings(serializer.validated_data)
            status_code = status.HTTP_200_OK
            message = message_codes.UMI_2000_REQUEST_SUCCESS_MESSAGE
            message_code = message_codes.UMI_2000_REQUEST_SUCCESS_CODE

        except (ParseError, JSONDecodeError) as ex:
            logger.error(f"JSON parsing error while retrieving booking list: {str(ex)}")
            status_code = status.HTTP_400_BAD_REQUEST
            message = message_codes.UMI_4002_INVALID_REQUEST_BODY_MESSAGE
            message_code = message_codes.UMI_4002_INVALID_REQUEST_BODY_CODE
            exception = ex

        except BookingException as ex:
            logger.error(f"Booking error in BookingListView: {ex.message} (code: {ex.message_code})")
            status_code = ex.status_code
            message = ex.message
            message_code = ex.message_code
            exception = ex

        except Exception as ex:
            logger.error(f"Unexpected error in BookingListView: {str(ex)}", exc_info=True)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_MESSAGE
            message_code = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_CODE
            exception = ex

        return log_and_respond(
            data=response_data,
            status=status_code,
            message=message,
            message_code=message_code,
            exception=exception
        )


class BookingCancelView(APIView):
    def post(self, request):
        exception = response_data = None
        try:
            serializer = BookingSerializer(data=request.data)

            if not serializer.is_valid():
                logger.error(f"Invalid cancellation data: {serializer.errors}")
                return log_and_respond(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=message_codes.UMI_4002_INVALID_REQUEST_BODY_MESSAGE,
                    message_code=message_codes.UMI_4002_INVALID_REQUEST_BODY_CODE,
                    error_info=format_serializer_errors(serializer.errors)
                )

            booking_id = serializer.validated_data['booking_id']

            cancel_booking(booking_id)
            logger.info(f"Booking cancelled successfully: {booking_id}")

            status_code = status.HTTP_200_OK
            message = message_codes.UMI_2000_REQUEST_SUCCESS_MESSAGE
            message_code = message_codes.UMI_2000_REQUEST_SUCCESS_CODE

        except (ParseError, JSONDecodeError) as ex:
            logger.error(f"JSON parsing error in BookingCancelView: {str(ex)}")
            status_code = status.HTTP_400_BAD_REQUEST
            message = message_codes.UMI_4002_INVALID_REQUEST_BODY_MESSAGE
            message_code = message_codes.UMI_4002_INVALID_REQUEST_BODY_CODE
            exception = ex

        except BookingException as ex:
            logger.error(f"Booking error in BookingCancelView: {ex.message} (code: {ex.message_code})")
            status_code = ex.status_code
            message = ex.message
            message_code = ex.message_code
            exception = ex

        except Exception as ex:
            logger.error(f"Unexpected error in BookingCancelView: {str(ex)}", exc_info=True)
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            message = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_MESSAGE
            message_code = message_codes.UMI_5000_INTERNAL_SERVER_ERROR_CODE
            exception = ex

        return log_and_respond(
            data=response_data,
            status=status_code,
            message=message,
            message_code=message_code,
            exception=exception
        )
