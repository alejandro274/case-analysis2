"""
Entrena un modelo de regresión para el GPA con un Pipeline:
- StandardScaler en numéricas
- (No hay categóricas string; todos los binarios/enteros van como numéricas)
- RandomForestRegressor
Guarda el artefacto en models/gpa_model.joblib
"""
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

from src.config import PROCESSED_DATA_PATH, MODEL_DIR, MODEL_PATH, FEATURES, TARGET

def main():
    if not os.path.exists(PROCESSED_DATA_PATH):
        raise FileNotFoundError("Ejecuta primero: python src/prepare_data.py")

    df = pd.read_csv(PROCESSED_DATA_PATH)

    # Todas las FEATURES son numéricas (enteros/binarios/continuas)
    numeric_features = FEATURES

    pre = ColumnTransformer(
        transformers=[("num", StandardScaler(), numeric_features)],
        remainder="drop"
    )

    model = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        n_jobs=-1
    )

    pipe = Pipeline([("pre", pre), ("model", model)])

    X = df[FEATURES].copy()
    y = df[TARGET].copy()

    X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe.fit(X_tr, y_tr)

    y_hat = pipe.predict(X_va)
    r2  = r2_score(y_va, y_hat)
    mae = mean_absolute_error(y_va, y_hat)
    print(f"[VAL] R2={r2:.3f} | MAE={mae:.3f} | n={len(y_va)}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"[OK] Modelo guardado en {MODEL_PATH}")

if __name__ == "__main__":
    main()