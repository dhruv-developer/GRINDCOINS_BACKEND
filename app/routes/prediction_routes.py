# app/routes/prediction_routes.py

from fastapi import APIRouter, UploadFile, File
import numpy as np
from app.services.prediction_service import predict_posture_from_video
from app.pose_utils import extract_keypoints_from_video

router = APIRouter()

@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Save uploaded video
    video_bytes = await file.read()
    with open("temp_video.mp4", "wb") as f:
        f.write(video_bytes)

    # Extract features
    features = extract_keypoints_from_video("temp_video.mp4")

    if features is None:
        return {"error": "Could not extract features from video."}

    # Predict posture
    prediction = predict_posture_from_video(np.array(features))

    return {"prediction": prediction}
