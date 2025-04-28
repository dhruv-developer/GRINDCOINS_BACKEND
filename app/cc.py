# import xgboost as xgb
# import joblib

# # Load your old model
# old_model = joblib.load("model.pkl")
# old_model2 = joblib.load("action_model.pkl")

# # Save it properly using XGBoost native save method
# old_model.save_model("model.json")  # IMPORTANT: save as .json
# old_model2.save_model("action_model.json")  # IMPORTANT: save as .json


# check_model.py
import joblib

obj = joblib.load("model.pkl")

print(type(obj))
print(obj)
