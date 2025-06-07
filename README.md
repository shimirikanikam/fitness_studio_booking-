Fitness Studio Booking API
A simple Booking API for a fictional fitness studio, built with Python and Django.
This API allows clients to view available classes, book a class, and view their bookings.


🚀 Setup Instructions
1. Clone the Repository
git clone https://github.com/shimirikanikam/fitness_studio_booking-.git
cd fitness-studio-booking-api

2. Create a Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Run the Application
python manage.py runserver

## 🗄️ Seed Data

- The application comes with sample data for classes and instructors.
- Data is stored in a Django SQLite database. 

🛠️ API Endpoints
1. Get All Classes
curl --location 'http://127.0.0.1:8000/app/class-list?timezone=America%2FNew_York' \
--data ''

Response:
{
    "code": 2000,
    "message": "Data retrieved successfully",
    "data": {
        "class_data": [
            {
                "id": "2",
                "name": "Evening Zumba",
                "date_time": "2025-06-08 08:36:58 EDT",
                "instructor": "Priya Kapoor",
                "available_slots": 10,
                "duration_minutes": 60
            }
        ]
    }
}

2. Book a Class

Request 

curl --location 'http://127.0.0.1:8000/app/book/' \
--header 'Authorization: Token 4e5e0a58b77e8f0b57a0b42bb2e56ef863d16c57' \
--header 'Content-Type: application/json' \
--data-raw '{
    "class_id": 1,
    "client_name":"Arjun kapoor",
    "client_email": "arjunkapoor549@gmail.com"
}'

response -


{
    "code": 2000,
    "message": "Class booked successfully.",
    "data": {
        "booking_id": "8",
        "class_id": "1",
        "class_name": "Morning Yoga",
        "instructor": "Aarav Mehta",
        "client_name": "Arjun kapoor",
        "client_email": "arjunkapoor549@gmail.com",
        "class_datetime": "2025-06-05 00:06:24 IST",
        "remaining_slots": 14
    }
}


3.Get Bookings by Email

Request

curl --location 'http://127.0.0.1:8000/app/bookings/?email=arjunkapoor549%40gmail.com' \
--data ''

Response -

{
    "code": 2000,
    "message": "Request Successful.",
    "data": {
        "bookings": [
            {
                "booking_id": 8,
                "client_email": "arjunkapoor549@gmail.com",
                "booking_time": "2025-06-07 18:02:31",
                "class_name": "Morning Yoga",
                "class_time": "2025-06-04 18:36:24",
                "instructor": "Aarav Mehta",
                "class_duration": 60
            }
        ]
    }
}


4. Cancel Booking API 
curl --location 'http://127.0.0.1:8000/app/cancel-booking/' \
--header 'Content-Type: application/json' \
--data '{
    "booking_id": 8
}'

   
Response -

{
    "code": 2000,
    "message": "Request Successful.",
    "data": {}
}
 






