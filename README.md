# actividad-ML

🎓 Predictor de Rendimiento Académico — ML + Streamlit (MVP)
Objetivo: predecir el GPA de estudiantes para:
Estudiantes: recibir un mensaje motivacional y acciones concretas de mejora.
Coordinadores: priorizar a quién apoyar (vista por lote + Top-N).
Ética: no usamos variables sensibles en el modelo; solo se emplean para auditoría interna de errores por subgrupos.

Estructura del proyecto:
case-analysis2/
├─ app/
│  └─ streamlit_app.py          # UI (vista Estudiante / Coordinador)
├─ data/
│  ├─ raw/                      # CSV original (NO subir a git)
│  └─ processed/                # CSV limpio (NO subir a git)
├─ models/                      # artefactos del modelo (.joblib, NO subir)
├─ src/
│  ├─ __init__.py               # ← importante para imports como paquete
│  ├─ config.py                 # rutas, columnas y umbrales
│  ├─ prepare_data.py           # limpieza/validación y guardado del CSV procesado
│  ├─ train.py                  # entrenamiento (Pipeline + RandomForest)
│  ├─ evaluate.py               # evaluación global + auditoría por subgrupos
│  ├─ predict.py                # utilidades de predicción + mapeo de GPA a clase
│  └─ recommendations.py        # mensajes motivacionales + tips accionables
├─ .gitignore
├─ requirements.txt
└─ README.md

requirements.txt incluye:
pandas
numpy
scikit-learn
joblib
streamlit
matplotlib


🗂️ Dataset
Ubica el CSV en: data/raw/student_performance.csv.
Columnas esperadas (resumen):
StudentID, Age, Gender, Ethnicity, ParentalEducation, StudyTimeWeekly, Absences, Tutoring, ParentalSupport, Extracurricular, Sports, Music, Volunteering, GPA, GradeClass

Objetivo de modelado: GPA (regresión).
Variables sensibles (auditoría interna únicamente): Gender, Ethnicity, ParentalEducation.

⚙️ Configuración (todo en src/config.py)
Ajusta aquí si cambian rutas, columnas o umbrales:
RAW_DATA_PATH        = "data/raw/student_performance.csv"
PROCESSED_DATA_PATH  = "data/processed/students_train.csv"
MODEL_DIR            = "models"
MODEL_PATH           = f"{MODEL_DIR}/gpa_model.joblib"

TARGET     = "GPA"
SENSITIVE  = ["Gender", "Ethnicity", "ParentalEducation"]   # auditoría interna
FEATURES   = ["Age","StudyTimeWeekly","Absences","Tutoring",
              "ParentalSupport","Extracurricular","Sports","Music","Volunteering"]

# Umbrales para clasificar la clase a partir del GPA predicho
RISK_THRESHOLDS = {"A": 3.5, "B": 3.0, "C": 2.5, "D": 2.0}


🚀 Cómo correr el pipeline

Importante: asegúrate de que exista src/__init__.py (aunque sea vacío)
y ejecuta desde la raíz del repo.

Preparar datos
python -m src.prepare_data

Entrenar modelo
python -m src.train
# imprime R2 y MAE de validación y guarda models/gpa_model.joblib


Evaluar + auditoría antibias
python -m src.evaluate
# imprime MAE total y MAE por subgrupos (Gender/Ethnicity/ParentalEducation si existen)

💻 Ejecutar la app (Streamlit)
Opción A (recomendada): exportar PYTHONPATH al lanzar
export PYTHONPATH=$(pwd)
streamlit run app/streamlit_app.py

Opción B: fijarlo en VS Code
Crea .env en la raíz con: PYTHONPATH=${workspaceFolder}
En Settings → “Python: Env File” → ${workspaceFolder}/.env
Abre nueva terminal y corre: streamlit run app/streamlit_app.py

Vistas
Estudiante: ingresa variables de hábito/esfuerzo →
muestra GPA esperado, clase (A–F), mensaje motivacional y tips accionables.
Coordinador: sube un CSV con columnas = FEATURES →
genera predicciones por lote, distribución por clase y Top-N estudiantes a priorizar (GPA más bajo).
Permite descargar el CSV con las predicciones.

☁️ Despliegue (rápido) en Streamlit Cloud
Conecta tu repo en Streamlit Cloud.
Main file: app/streamlit_app.py
Python version: 3.9/3.10
Requirements: el archivo requirements.txt del repo.
Variable de entorno (si hace falta): PYTHONPATH=/app/case-analysis2 (ajusta a la ruta que muestre el panel).

