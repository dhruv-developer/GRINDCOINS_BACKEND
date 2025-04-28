import io
from app.db.mongodb import faces_collection
from backy.app.face_utils import extract_face, get_embedding, find_match
from fastapi import UploadFile
import numpy as np

async def register_face(file: UploadFile, name: str):
    contents = await file.read()
    face = extract_face(io.BytesIO(contents))
    if face is None:
        return {"error": "No face detected"}

    emb = get_embedding(face)
    emb_list = emb.tolist()

    faces_collection.insert_one({
        "name": name,
        "embedding": emb_list
    })

    return {"message": f"Face for {name} registered successfully."}

async def recognize_face(file: UploadFile):
    contents = await file.read()
    face = extract_face(io.BytesIO(contents))
    if face is None:
        return {"error": "No face detected"}

    emb = get_embedding(face)
    db_faces = list(faces_collection.find({}))

    if not db_faces:
        return {"error": "No faces registered in the database."}

    name, distance = find_match(emb, db_faces)

    return {
        "recognized_as": name,
        "distance": round(float(distance), 2)
    }
