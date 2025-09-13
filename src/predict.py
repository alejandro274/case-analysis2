"""
Carga el modelo entrenado y expone funciones de predicción.
"""
import os
import joblib
import pandas as pd
from src.config import MODEL_PATH, FEATURES, RISK_THRESHOLDS

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("No se encontró el modelo. Ejecuta src/train.py")
    return joblib.load(MODEL_PATH)

def predict_one(model, features: dict) -> float:
    # features: dict con claves EXACTAS = FEATURES
    row = pd.DataFrame([features], columns=FEATURES)
    return float(model.predict(row)[0])

def map_gpa_to_grade(gpa: float) -> str:
    # Usa los umbrales oficiales del dataset
    if gpa >= RISK_THRESHOLDS["A"]:
        return "A"
    if gpa >= RISK_THRESHOLDS["B"]:
        return "B"
    if gpa >= RISK_THRESHOLDS["C"]:
        return "C"
    if gpa >= RISK_THRESHOLDS["D"]:
        return "D"
    return "F"