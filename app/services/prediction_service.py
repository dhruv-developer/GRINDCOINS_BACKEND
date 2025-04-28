import shutil
import uuid
import os
import numpy as np
import joblib
from app.pose_utils import extract_keypoints_from_video

# Load model once
model_data = joblib.load("app/model.pkl")
model = model_data["model"]

async def predict_posture_from_video(file):
    if file.content_type != "video/mp4":
        return {"error": "Only MP4 videos are supported"}

    temp_video_path = f"temp_{uuid.uuid4().hex}.mp4"
    with open(temp_video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        keypoints = extract_keypoints_from_video(temp_video_path)
        if keypoints is None:
            return {"error": "No keypoints detected"}

        pred_proba = model.predict_proba([keypoints])[0]
        pred_index = np.argmax(pred_proba)
        prediction = model.classes_[pred_index]
        confidence = round(float(pred_proba[pred_index]) * 100, 2)

        return {
            "posture": str(prediction),
            "confidence_percent": confidence
        }
    finally:
        os.remove(temp_video_path)
