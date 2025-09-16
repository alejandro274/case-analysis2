"""
App MVP con dos vistas:
- Estudiante: predicción de GPA + mensaje motivacional + tips.
- Coordinador: carga CSV (sin sensibles para el modelo) -> lote de predicciones,
  distribución de riesgos y TOP-N estudiantes a priorizar.
"""
import io
import pandas as pd
import streamlit as st
from src.config import FEATURES
from src.predict import load_model, predict_one, map_gpa_to_grade
from src.recommendations import student_message, actionable_tips

st.set_page_config(page_title="Predictor Académico", layout="centered")
st.title("🎓 Predictor de Rendimiento Académico")

tab1, tab2 = st.tabs(["Estudiante", "Coordinador"])

# -------------------- Vista Estudiante --------------------
with tab1:
    st.subheader("Vista Estudiante")
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Edad", 15, 18, 16)
        study = st.slider("Horas de estudio / semana", 0, 20, 8)
        absences = st.slider("Inasistencias (año)", 0, 30, 8)
        tutoring = st.selectbox("¿Recibe tutoría?", ["No", "Sí"])
    with col2:
        psup = st.select_slider("Apoyo parental (0-4)", options=[0,1,2,3,4], value=2)
        extra = st.selectbox("¿Extracurricular?", ["No","Sí"])
        sports = st.selectbox("¿Deportes?", ["No","Sí"])
        music = st.selectbox("¿Música?", ["No","Sí"])
        volun = st.selectbox("¿Voluntariado?", ["No","Sí"])

    if st.button("Predecir GPA"):
        model = load_model()
        features = {
            "Age": age,
            "StudyTimeWeekly": float(study),
            "Absences": int(absences),
            "Tutoring": 1 if tutoring=="Sí" else 0,
            "ParentalSupport": int(psup),
            "Extracurricular": 1 if extra=="Sí" else 0,
            "Sports": 1 if sports=="Sí" else 0,
            "Music": 1 if music=="Sí" else 0,
            "Volunteering": 1 if volun=="Sí" else 0,
        }
        gpa = predict_one(model, features)
        grade = map_gpa_to_grade(gpa)

        st.metric("GPA esperado", f"{gpa:.2f}")
        st.write(f"**Clase esperada:** {grade}")
        st.info(student_message(grade))
        st.write("**Siguientes pasos recomendados:**")
        for t in actionable_tips(features):
            st.write(f"- {t}")

# -------------------- Vista Coordinador --------------------
with tab2:
    st.subheader("Vista Coordinador (priorización de riesgo)")
    st.caption("Sube un CSV con columnas: " + ", ".join(FEATURES))
    up = st.file_uploader("Cargar CSV", type=["csv"])
    top_n = st.slider("Top N a priorizar (GPA más bajo)", 5, 50, 10)

    if up is not None:
        model = load_model()
        df = pd.read_csv(up)

        # Validación rápida de columnas
        missing = [c for c in FEATURES if c not in df.columns]
        if missing:
            st.error(f"Faltan columnas en el CSV: {missing}")
        else:
            # Predicciones
            preds = []
            for _, r in df.iterrows():
                row = {c: r[c] for c in FEATURES}
                gpa = predict_one(model, row)
                preds.append(gpa)
            df["GPA_pred"] = preds
            df["Grade_pred"] = df["GPA_pred"].apply(map_gpa_to_grade)

            # Distribución por clase
            dist = df["Grade_pred"].value_counts().rename_axis("Grade").reset_index(name="count")
            st.write("### Distribución de riesgo (predicho)")
            st.dataframe(dist)

            # Top-N a intervenir (menor GPA primero)
            st.write(f"### Top {top_n} estudiantes a priorizar")
            st.dataframe(df.sort_values("GPA_pred").head(top_n))

            # Descarga de resultados
            buf = io.StringIO()
            df.to_csv(buf, index=False)
            st.download_button("Descargar predicciones CSV", buf.getvalue(), file_name="predicciones.csv", mime="text/csv")
