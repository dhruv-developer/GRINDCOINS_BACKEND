import cv2
import numpy as np
from mediapipe import solutions

mp_pose = solutions.pose
pose = mp_pose.Pose(static_image_mode=True)

def extract_pose_keypoints(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(img_rgb)

    if result.pose_landmarks:
        keypoints = []
        for lm in result.pose_landmarks.landmark:
            keypoints.extend([lm.x, lm.y, lm.z, lm.visibility])
        return keypoints
    return None

def normalize_keypoints(keypoints):
    keypoints = np.array(keypoints).reshape(-1, 4)
    center = keypoints[0][:2]
    for i in range(len(keypoints)):
        keypoints[i][:2] -= center
    return keypoints.flatten()
