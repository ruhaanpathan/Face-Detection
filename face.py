import cv2
import face_recognition
import os

# Directory to store the known faces
known_faces_dir = "known_faces"
os.makedirs(known_faces_dir, exist_ok=True)


# Step 1: Capture a photo for registration
def capture_photo():
    video_capture = cv2.VideoCapture(0)

    print("Press 's' to take a photo or 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        cv2.imshow("Capture Photo", frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            photo_path = os.path.join(known_faces_dir, "registered_face.jpg")
            cv2.imwrite(photo_path, frame)
            print("Photo saved!")
            break
        elif key == ord('q'):
            print("Exiting without saving.")
            video_capture.release()
            cv2.destroyAllWindows()
            return None

    video_capture.release()
    cv2.destroyAllWindows()
    return photo_path


# Step 2: Load known face encoding
def load_known_face(photo_path):
    known_image = face_recognition.load_image_file(photo_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]
    return known_encoding


# Step 3: Recognize the face in real-time
def recognize_face(known_encoding):
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame)
            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces([known_encoding], face_encoding)
                name = "Unknown"

                if True in matches:
                    name = "Registered"

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Main Function
def main():
    photo_path = capture_photo()
    if photo_path:
        known_encoding = load_known_face(photo_path)
        recognize_face(known_encoding)


if _name_ == "_main_":
    main()