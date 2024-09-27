import face_recognition
import cv2
import numpy as np

# Initialize variables
known_face_encodings = []
known_face_names = []
serial_number = 1

# Initialize the camera
video_capture = cv2.VideoCapture(0)

# Helper function to add a new person
def register_new_person(face_encoding):
    global serial_number
    known_face_encodings.append(face_encoding)
    known_face_names.append(f"Person {serial_number}")
    serial_number += 1

while True:
    # Capture a frame from the video feed
    ret, frame = video_capture.read()
    
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

    if face_locations:
        try:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            print(f"Face encodings: {face_encodings}")  # Debugging: check encodings
        except Exception as e:
            print(f"Error during face encoding: {e}")
            face_encodings = []
    else:
        face_encodings = []

    for face_encoding in face_encodings:
        # Check if this face matches any previously known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
       
