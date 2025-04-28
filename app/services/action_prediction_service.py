import os
import shutil
import uuid
import cv2
import numpy as np
import joblib
from app.action_pose_utils import extract_pose_keypoints, normalize_keypoints
from moviepy.editor import VideoFileClip

# ✅ Load model and label encoder from tuple
model_data = joblib.load("app/action_model.pkl")
model = model_data[0]  # Access by index, NOT by key
label_encoder = model_data[1]  # Access by index

async def predict_action_from_video(file):
    if file.content_type != "video/mp4":
        return {"error": "Only MP4 videos are supported"}

    temp_video_path = f"temp_{uuid.uuid4().hex}.mp4"
    with open(temp_video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    temp_frame_path = f"frame_{uuid.uuid4().hex}.jpg"

    try:
        # Extract a middle frame from the video
        clip = VideoFileClip(temp_video_path)
        frame = clip.get_frame(clip.duration / 2)
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(temp_frame_path, frame_bgr)

        # Extract and normalize keypoints
        keypoints = extract_pose_keypoints(temp_frame_path)
        if keypoints is None:
            return {"error": "No keypoints detected"}

        normalized_keypoints = normalize_keypoints(keypoints)

        # Predict
        pred_proba = model.predict_proba([normalized_keypoints])[0]
        pred_index = np.argmax(pred_proba)
        prediction = label_encoder.inverse_transform([pred_index])[0]
        confidence = round(float(pred_proba[pred_index]) * 100, 2)

        return {
            "action": str(prediction),
            "confidence_percent": confidence
        }

    finally:
        # Cleanup temp files
        os.remove(temp_video_path)
        if os.path.exists(temp_frame_path):
            os.remove(temp_frame_path)
