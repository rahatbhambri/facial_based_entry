import random
import string
from database.db import get_connection

db = get_connection()

def generate_random_string(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))

def get_all_bookings(user_id):
    tickets_data = list(db.tickets.find({"user_id": str(user_id)}))
    print("All tickets booked for user: ", user_id)
    for t in tickets_data:
        print(t.get("ticket_id"), t.get("booking_time"))

def get_all_cinemas():
    return list(db.cinemas.find({}, {"_id":0, "name": 1, "cinema_id": 1}))