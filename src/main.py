from database.db import get_connection

def main():
    db = get_connection()

    # Example: Create a collection and insert a document
    users_collection = db.users
    users_collection.insert_one({'name': 'Alice', 'age': 30})

    # Example: Query the collection
    users = users_collection.find()
    for user in users:
        print(user)

if __name__ == "__main__":
    main()