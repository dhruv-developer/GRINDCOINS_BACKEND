import random
import io
import numpy as np
from app.db.mongodb import db
from app.utils.email_utils import send_otp_email
from app.face_utils import extract_face, get_embedding, find_match

users_collection = db["users"]

async def signup_user(file, email, name):
    if users_collection.find_one({"email": email}):
        return {"error": "Email already registered."}

    contents = await file.read()
    face = extract_face(io.BytesIO(contents))
    if face is None:
        return {"error": "No face detected."}

    emb = get_embedding(face).tolist()
    otp = str(random.randint(100000, 999999))

    users_collection.insert_one({
        "email": email,
        "name": name,
        "embedding": emb,
        "otp": otp,
        "verified": False,
        "coins" : 0
    })

    send_otp_email(email, otp)

    return {"message": "Signup successful. OTP sent to your email."}

async def verify_otp(email, otp):
    user = users_collection.find_one({"email": email})
    if not user:
        return {"error": "User not found."}

    if user["otp"] != otp:
        return {"error": "Invalid OTP."}

    users_collection.update_one({"email": email}, {"$set": {"verified": True}})
    return {"message": "Email verified successfully."}

async def login_user(file, email):
    user = users_collection.find_one({"email": email, "verified": True})
    if not user:
        return {"error": "User not found or email not verified."}

    contents = await file.read() if file else None
    if contents:
        face = extract_face(io.BytesIO(contents))
        if face is None:
            return {"error": "No face detected."}

        emb = get_embedding(face)
        name, distance = find_match(emb, [{"embedding": user["embedding"], "name": user["name"]}], limit=8)

        if name == "Unknown":
            return {"error": "Face does not match."}

    return {
        "message": f"Welcome back, {user['name']}!",
        "name": user["name"],      # ✅
        "email": user["email"]     # ✅
    }
