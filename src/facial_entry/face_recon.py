import face_recognition
import cv2, json
import numpy as np
from database.db import get_connection
from . import load_faces


class FaceRecognizer:
    def __init__(self):
        # Initialize variables
        self.known_face_encodings, self.known_face_id = load_faces.fetch_all_encodings()
        self.serial_number = 1

        # Initialize the camera
        self.video_capture = cv2.VideoCapture(0)
        self.db = get_connection()
        print("here")

    # Helper function to add a new person
    def register_new_person(self, face_encoding, name, ticket):
        self.known_face_encodings.append(face_encoding)
        
        # Convert face encoding to a list
        face_encoding_list = face_encoding.tolist()
        # Convert the list to a JSON string
        face_encoding_str = json.dumps(face_encoding_list)

        self.db.users.insert_one({
            'face_encoding': face_encoding_str,
            'name' : name, 
            'ticket_id': ticket})


    # def register_ticket_via_face(self)
    # def validate_face(self)
    
    def detect_ticket_via_face(self):
        reocurring_user = False
        while True:
            # Capture a frame from the video feed
            ret, frame = self.video_capture.read()
            if not ret:
                print("Failed to grab frame")
                break
            # Resize the frame to speed up the face recognition process
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image to RGB
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            # Debugging: Check the shape and type of rgb_small_frame
            print(f"rgb_small_frame shape: {rgb_small_frame.shape}, dtype: {rgb_small_frame.dtype}")
            # Find all face locations and face encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            print(f"Face locations: {face_locations}")
            face_encodings = []
            # If face is detected then get face encodings
            if face_locations:
                try:
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    print(f"Face encodings: {face_encodings}")  # Debugging: check encodings
                except Exception as e:
                    print(f"Error during face encoding: {e}")
    
            # Process each detected face
            for face_encoding in face_encodings:
                # Check if this face matches any previously known face
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    id = self.known_face_id[first_match_index]
                    user_data = self.db.users.find_one({"_id": id})
                    name = user_data["name"]
                    
                    tickets_data = list(self.db.tickets.find({"user_id": str(id)}))
                    print("All tickets booked for user: ")
                    for t in tickets_data:
                        print(t.get("ticket_id"), t.get("booking_time"))
                                                            
                    reocurring_user = True
                    break
                else:
                    print("No registered ticket found")


                # Draw a box around the face
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the result frame
            cv2.imshow('Video', frame)

            # Exit the loop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if reocurring_user:
                break

        # Release the camera and close any OpenCV windows
        self.video_capture.release()
        cv2.destroyAllWindows()


# func1: Register ticket(ID) via face  - clientSide
# func2: Detect ticket via face - ServerSide/ on premises
# Table tickets - (ticket_id, audi, time, seat no.)
# cinemas - cinema_id, name, audis


    def register_face_with_ticket(self):
        reocurring_user = False
        while True:
            # Capture a frame from the video feed
            ret, frame = self.video_capture.read()
            if not ret:
                print("Failed to grab frame")
                break
            # Resize the frame to speed up the face recognition process
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image to RGB
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
            # Debugging: Check the shape and type of rgb_small_frame
            print(f"rgb_small_frame shape: {rgb_small_frame.shape}, dtype: {rgb_small_frame.dtype}")
            # Find all face locations and face encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_small_frame)
            print(f"Face locations: {face_locations}")
            face_encodings = []
            # If face is detected then get face encodings
            if face_locations:
                try:
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    print(f"Face encodings: {face_encodings}")  # Debugging: check encodings
                except Exception as e:
                    print(f"Error during face encoding: {e}")
    
                # Process each detected face
                for face_encoding in face_encodings:
                    # If no match is found, prompt for the new person's name
                    name = input("New face detected! Please enter the name: ")
                    ticket = input("Please enter your ticket number")
                    # pancard = input("Input pancard")
                    self.register_new_person(face_encoding, name, ticket)
                break
            
            # Display the result frame
            cv2.imshow('Video', frame)

            # Exit the loop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            if reocurring_user:
                break

        # Release the camera and close any OpenCV windows
        self.video_capture.release()
        cv2.destroyAllWindows()
    



