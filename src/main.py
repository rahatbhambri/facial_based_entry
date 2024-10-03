from facial_entry import face_recon

def main():
    FaceRec = face_recon.FaceRecognizer()
    option = input("""Welcome to the portal, press 1 to register new ticket, \n 2 to detect a ticket \n""")
    try:
        option = int(option)
        if option == 1:
            FaceRec.register_ticket_with_face()
        elif option == 2:
            FaceRec.detect_ticket_via_face()
        else:
            print("invalid ticket")
    except:
        print("invalid ticket")

if __name__ == "__main__":
    main()