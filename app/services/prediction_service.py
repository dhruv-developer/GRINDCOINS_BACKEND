# app/services/prediction_service.py

from xgboost import Booster
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load XGBoost model safely
from xgboost import XGBClassifier

# Step 1: Load the .pkl file
obj = joblib.load("app/model.pkl")  # or "./app/model.pkl" depending on structure

# Step 2: Extract components
model: XGBClassifier = obj['model']
label_encoder: LabelEncoder = obj['label_encoder']

# Now you can define your function

def predict_posture_from_video(features: np.ndarray) -> str:
    """
    Given extracted video features, predict the posture class.

    Args:
        features (np.ndarray): Input feature vector.

    Returns:
        str: Predicted posture label.
    """
    # Reshape features properly
    features = features.reshape(1, -1)  # Make it 2D for prediction

    # Predict label
    pred = model.predict(features)

    # Decode label back to original class name
    predicted_label = label_encoder.inverse_transform(pred)[0]

    return predicted_label
