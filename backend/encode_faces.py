import os
import pickle
import face_recognition

# Paths
dataset_path = "dataset" # your dataset folder
models_path = "models/face_recognition_model.pkl"  # file to save encodings

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
                print(f"Encoded {image_name} for {person_name}")
            else:
                print(f"No face found in {image_name}")

    return known_face_encodings, known_face_names

# Encode faces and save
encodings, names = encode_faces(dataset_path)
with open(models_path, "wb") as f:
    pickle.dump((encodings, names), f)

print(f"\nAll faces encoded and saved to {models_path}")