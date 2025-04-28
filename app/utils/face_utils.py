import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet
from PIL import Image
from numpy.linalg import norm

detector = MTCNN()
embedder = FaceNet()

def extract_face(file, required_size=(160, 160)):
    image = Image.open(file)
    image = image.convert('RGB')
    pixel = np.asarray(image)
    results = detector.detect_faces(pixel)
    if len(results) == 0:
        return None
    x1, y1, width, height = results[0]['box']
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = pixel[y1:y2, x1:x2]
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = np.asarray(image)
    return face_array

def get_embedding(face_pixel):
    face_pixels = face_pixel.astype('float32')
    samples = np.expand_dims(face_pixels, axis=0)
    emb = embedder.embeddings(samples)
    return emb[0]

def find_match(emb_new, db_faces, limit=10):
    min_dist = float('inf')
    identity = 'Unknown'
    for entry in db_faces:
        db_emb = np.array(entry["embedding"])
        db_name = entry["name"]
        dist = norm(emb_new - db_emb)
        if dist < min_dist:
            min_dist = dist
            identity = db_name
    if min_dist > limit:
        identity = 'Unknown'
    return identity, min_dist
