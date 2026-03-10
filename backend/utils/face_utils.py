import cv2
import face_recognition
import numpy as np
import os

def encode_faces(dataset_path):
    known_face_encodings = []
    known_face_names = []

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)

        if not os.path.isdir(person_path):
            continue

        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_face_encodings.append(encodings[0])
                known_face_names.append(person_name)

    return known_face_encodings, known_face_names


def identify_face(image, known_face_encodings, known_face_names):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    for face_encoding in face_encodings:
        distances = face_recognition.face_distance(known_face_encodings, face_encoding)

        if len(distances) == 0:
            return "No Data", 0

        best_match_index = np.argmin(distances)
        confidence = round((1 - distances[best_match_index]) * 100, 2)

        if distances[best_match_index] < 0.5:
            return known_face_names[best_match_index], confidence

    return "Unknown", 0