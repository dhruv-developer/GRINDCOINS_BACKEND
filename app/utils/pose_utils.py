# app/pose_utils.py

import cv2
import mediapipe as mp
import numpy as np

def extract_keypoints_from_video(video_path: str) -> np.ndarray:
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    cap = cv2.VideoCapture(video_path)
    keypoints = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            frame_keypoints = []
            for landmark in results.pose_landmarks.landmark:
                frame_keypoints.extend([landmark.x, landmark.y, landmark.z, landmark.visibility])
            keypoints.append(frame_keypoints)

    cap.release()

    if keypoints:
        return np.mean(keypoints, axis=0)  # Mean pooling across frames
    else:
        return None
