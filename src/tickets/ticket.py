from .utils import generate_random_string
from database.db import get_connection


class TicketGenerator:
    def __init__(self, movie_id, cinema_id, date):
        self.ticket_id = generate_random_string(8)
        self.date = date
        self.movie_id = movie_id
        self.cinema_id = cinema_id
        self.db = get_connection()
        
    
    def getTicketId(self):
        return self.ticket_id
    
    def updateDbForTicket(self): 
        movie_name = self.db.movies.find_one({"movie_id": self.movie_id})
        self.db.tickets.insert_one({"ticket_id": self.ticket_id})
        
    