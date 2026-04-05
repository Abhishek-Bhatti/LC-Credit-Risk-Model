import joblib
import pandas as pd

def load_ml_assets(file_path="lending_model_final.pkl"):
    """Loads the XGBoost model and feature names."""
    data = joblib.load(file_path)
    return data['model'], data['features']

def get_ml_prediction(model, features, data_list):
    """Returns the probability of repayment."""
    df = pd.DataFrame([data_list], columns=features)
    return model.predict_proba(df)[0, 1]