from facial_entry import face_recon
from tickets.ticket import TicketGenerator
from database.db import get_connection

def main():
    
    db = get_connection()
    FaceRec = face_recon.FaceRecognizer()
    FaceRec.login_via_face()
    user_id = FaceRec.user_id
    
    cinemas = list(db.cinemas.find({}, {"_id":0, "name": 1, "cinema_id": 1}))
    for i, c in enumerate(cinemas):
        print(i+1, c.get("name"))
    id = int(input("enter cinema id to proceed "))
    c_id = cinemas[id-1].get("cinema_id") 
    
    
    
    
    TicketGen = TicketGenerator(c_id)
    quantity = int(input("enter number of people"))
    TicketGen.BookTickets(user_id, 1234, quantity)
    
    
    # tickets_data = list(self.db.tickets.find({"user_id": str(id)}))
    #                 print("All tickets booked for user: ")
    #                 for t in tickets_data:
    #                     print(t.get("ticket_id"), t.get("booking_time"))
                                                            
                                                            
if __name__ == "__main__":
    main()