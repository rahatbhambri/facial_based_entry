from database.db import get_connection
from facial_entry import face_recon

def main():
    FaceRec = face_recon.FaceRecognizer()
    FaceRec.start_capture()
    pass

if __name__ == "__main__":
    main()