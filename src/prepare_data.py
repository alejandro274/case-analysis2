
# Lee el CSV crudo, valida columnas, normaliza si hiciera falta
# Guarda un CSV procesado con sólo las columnas necesarias, llamado "students_train.csv".

import os
import pandas as pd
from config import (
    RAW_DATA_PATH, PROCESSED_DATA_PATH, FEATURES, TARGET,
    SENSITIVE, PERCENT_TO_UNIT, HUNDRED_TO_UNIT
)

def load_raw(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró {path}. Coloca tu CSV en data/raw/")
    return pd.read_csv(path)

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Si hubiera columnas en 0–100, pasarlas a 0–1
    for c in PERCENT_TO_UNIT + HUNDRED_TO_UNIT:
        if c in df.columns and df[c].max() > 1.0:
            df[c] = df[c] / 100.0
    return df

def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Verificamos que existan todas las columnas críticas
    required = FEATURES + [TARGET]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en el CSV: {missing}")

    # Conservamos sensibles para auditoría (no las usará el modelo)
    audit_cols = [c for c in SENSITIVE if c in df.columns]
    keep = FEATURES + [TARGET] + audit_cols
    return df[keep].copy()

def main():
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)

    df = load_raw(RAW_DATA_PATH)
    df = normalize_columns(df)
    df = select_columns(df)

    # Quita filas sin objetivo
    df = df.dropna(subset=[TARGET]).reset_index(drop=True)

    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"[OK] Guardado procesado en {PROCESSED_DATA_PATH} | filas={len(df)}")

if __name__ == "__main__":
    main()