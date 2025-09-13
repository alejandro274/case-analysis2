
# Config central del proyecto — aquí viven las rutas, columnas y reglas.
# Ajustar aquí si cambian nombres del archivo o umbrales.
# Yo puse como nombre del archivo "student_performance.csv" para que sea facil de escribir


from typing import List

# Rutas
RAW_DATA_PATH = "data/raw/student_performance.csv"
PROCESSED_DATA_PATH = "data/processed/students_train.csv"
MODEL_DIR = "models"
MODEL_PATH = f"{MODEL_DIR}/gpa_model.joblib"

# Objetivo de negocio: predecir GPA (regresión)
TARGET: str = "GPA"

# Variables sensibles por razones éticas: NO entran al modelo; sólo para auditoría interna
SENSITIVE: List[str] = ["Gender", "Ethnicity", "ParentalEducation"]

# Features que SÍ usaremos (académicas/hábitos/esfuerzo)
FEATURES: List[str] = [
    "Age",
    "StudyTimeWeekly",
    "Absences",
    "Tutoring",
    "ParentalSupport",
    "Extracurricular",
    "Sports",
    "Music",
    "Volunteering",
]

# (por si vinieran en 0-100; en el CSV ya están en rangos adecuados)
PERCENT_TO_UNIT: List[str] = []        # ej. ["attendance_rate"]
HUNDRED_TO_UNIT: List[str] = []        # ej. ["quiz_avg", "exam_avg"]

# Umbrales para mapear GPA predicho a riesgo (coordinador)
# Nota: el dataset define GradeClass con: A(>=3.5), B[3.0,3.5), C[2.5,3.0), D[2.0,2.5), F<2.0
RISK_THRESHOLDS = {
    "A": 3.5,
    "B": 3.0,
    "C": 2.5,
    "D": 2.0,
}