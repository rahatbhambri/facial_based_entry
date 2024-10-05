from facial_entry import face_recon
from tickets.ticket import TicketGenerator
from database.db import get_connection

def main():
    
    db = get_connection()
    cinemas = list(db.cinemas.find({}, {"_id":0, "name": 1, "cinema_id": 1}))
    for i, c in enumerate(cinemas):
        print(i+1, c.get("name"))
    id = int(input("enter cinema id to proceed "))
    c_id = cinemas[id-1].get("cinema_id") 
    
    TicketGen = TicketGenerator(c_id)
    TicketGen.BookTicket("66fe5976009944b3f1e02b2a", 1234)
    
    FaceRec = face_recon.FaceRecognizer()
    # Your face becomes your ticket 
    option = input("""Welcome to the portal, press 1 to register new ticket, \n 2 to detect a ticket \n""")
    
    
    try:
        option = int(option)
        if option == 1:
            FaceRec.register_face_with_ticket()
        elif option == 2:
            FaceRec.detect_ticket_via_face()
        else:
            print("invalid ticket")
    except:
        print("invalid ticket")

if __name__ == "__main__":
    main()