
from database.db import get_connection
import json

def fetch_all_encodings():
    db = get_connection()
    
    encodings = []
    names = []
    # Example: Create a collection and insert a document
    users_data = db.users.find()
    for user in users_data:
        str_e = user.get("face_encoding") 
        e = json.loads(str_e)
        n = user.get("name")
        encodings.append(e)
        names.append(n)
        
    return encodings, names
    
    
    
    
    