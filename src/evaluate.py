"""
Evalúa rendimiento global (MAE) y MAE por subgrupos de variables sensibles.
Esto NO se muestra al estudiante; es para control interno (ética).
"""
import os
import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error
from src.config import PROCESSED_DATA_PATH, MODEL_PATH, FEATURES, TARGET, SENSITIVE

def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Entrena primero con src/train.py")
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(PROCESSED_DATA_PATH)

    X, y = df[FEATURES], df[TARGET]
    y_hat = model.predict(X)

    mae_total = mean_absolute_error(y, y_hat)
    print(f"[TOTAL] MAE={mae_total:.3f} (n={len(y)})")

    for s in SENSITIVE:
        if s in df.columns:
            print(f"\n== Auditoría por {s} ==")
            for grp, sdf in df.groupby(s):
                mae_g = mean_absolute_error(sdf[TARGET], model.predict(sdf[FEATURES]))
                print(f"  {s}={grp}: n={len(sdf)} | MAE={mae_g:.3f}")

if __name__ == "__main__":
    main()