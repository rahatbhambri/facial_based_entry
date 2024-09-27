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
def register_new_person(face_encoding, name):
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

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

    face_encodings = []
    if face_locations:
        try:
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            print(f"Face encodings: {face_encodings}")  # Debugging: check encodings
        except Exception as e:
            print(f"Error during face encoding: {e}")

    # Process each detected face
    for face_encoding in face_encodings:
        # Check if this face matches any previously known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        else:
            # If no match is found, prompt for the new person's name
            name = input("New face detected! Please enter the name: ")
            register_new_person(face_encoding, name)

        # Display the name on the frame
        print(f"Detected: {name}")

        # Draw a box around the face
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the result frame
    cv2.imshow('Video', frame)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close any OpenCV windows
video_capture.release()
cv2.destroyAllWindows()
