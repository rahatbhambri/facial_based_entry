from database.db import get_connection
from facial_entry import face_recon

def main():
    FaceRec = face_recon.FaceRecognizer()
    FaceRec.login_via_face()
    user_id = FaceRec.user_id
    
    ip = input("Retrieve all bookings y/n ?")
    if ip in ["y", "Y"]:
        get_all_bookings(user_id=user_id)
    
    cinemas = get_all_cinemas()
    for i, c in enumerate(cinemas):
        print(i+1, c.get("name"))
    id = int(input("enter cinema id to proceed "))
    c_id = cinemas[id-1].get("cinema_id") 
    
    print("Movies available at your selected cinema:- ")
    movies = get_all_movies()
    for i, m in enumerate(movies):
        print(i+1, m.get("name"))
    id = int(input("enter movie id to proceed "))
    m_id = movies[id-1].get("movie_id") 
    
    
    TicketGen = TicketGenerator(c_id)
    quantity = int(input("enter number of people"))
    TicketGen.BookTickets(user_id, m_id, quantity)
                                                       
                                                            
if __name__ == "__main__":
    main()