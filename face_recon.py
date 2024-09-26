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

    # Resize the frame to speed up the face recognition process
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image to RGB (required for face_recognition)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Process each face found in the frame
    for face_encoding in face_encodings:
        # Check if this face matches any previously known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, use the known person's serial number
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        else:
            # If no match is found, register the new person
            register_new_person(face_encoding)
            name = known_face_names[-1]

        # Display the serial number on the video
        print(f"Detected: {name}")

    # Display the result frame
    cv2.imshow('Video', frame)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
