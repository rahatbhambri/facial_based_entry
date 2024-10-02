from facial_entry import face_recon

def main():
    FaceRec = face_recon.FaceRecognizer()
    FaceRec.register_ticket_with_face()
    pass

if __name__ == "__main__":
    main()