import cv2
import face_recognition
import os
import numpy as np


def load_known_faces(directory: str):
    known_encodings = []
    known_names = []
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if not os.path.isfile(filepath):
            continue
        # 拡張子を除いたファイル名を人物名として使用する
        name, _ = os.path.splitext(file)
        image = face_recognition.load_image_file(filepath)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)
    return known_encodings, known_names


def main():
    known_faces_dir = os.path.join(os.path.dirname(__file__), "known_faces")
    if not os.path.isdir(known_faces_dir):
        print(f"Known faces directory '{known_faces_dir}' not found")
        return

    known_encodings, known_names = load_known_faces(known_faces_dir)
    if not known_encodings:
        print("No known faces found in the directory.")
        return

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Unable to access the camera")
        return

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            # OpenCV が使用する BGR から RGB へ変換する
            rgb_frame = frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                if face_distances.size > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                face_names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 2, bottom - 5), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), 1)

            cv2.imshow('Real-Time Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
