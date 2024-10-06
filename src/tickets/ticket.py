from utils.utils import generate_random_string
from database.db import get_connection
from datetime import datetime


class TicketGenerator:
    def __init__(self, cinema_id):
        self.cinema_id = cinema_id
        self.db = get_connection()
        
    
    def getTicketId(self):
        return self.ticket_id
    
    def BookTickets(self, user_id, movie_id, quan): 
        documents= []
        for q in range(quan):
            ticket_id = generate_random_string(8)
            documents.append({"ticket_id": ticket_id, "movie_id" : movie_id, 
                                        "user_id": user_id, "booking_time": datetime.now()})
            print("booked ticket", ticket_id, "for user")
        
        self.db.tickets.insert_many(documents=documents)
    