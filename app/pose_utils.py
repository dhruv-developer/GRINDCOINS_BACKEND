import cv2
import numpy as np
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)

def extract_keypoints_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    all_keypoints = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            keypoints = []
            for lm in results.pose_landmarks.landmark:
                keypoints.append([lm.x, lm.y, lm.z])
            keypoints = np.array(keypoints)

            normalized = normalize_keypoints(keypoints)
            all_keypoints.append(normalized)

    cap.release()
    return np.mean(all_keypoints, axis=0) if all_keypoints else None

def normalize_keypoints(keypoints):
    center = keypoints[0]  # using nose as origin
    normalized = keypoints - center
    return normalized.flatten()
