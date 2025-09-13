"""
Mensajes motivacionales + acciones concretas, personalizadas con inputs.
Nunca basadas en atributos sensibles.
"""
def student_message(grade: str) -> str:
    msgs = {
        "A": "¡Vas excelente! Mantén hábitos y comparte lo que te funciona.",
        "B": "Muy bien. Con pequeños ajustes puedes rozar la excelencia.",
        "C": "Estás a mitad de camino. Enfócate en consistencia semanal.",
        "D": "Aún hay tiempo. Con apoyo y plan claro, puedes remontar.",
        "F": "No estás solo. Construyamos un plan de mejora accionable.",
    }
    return msgs.get(grade, "Sigue adelante, paso a paso.")

def actionable_tips(features: dict):
    tips = []
    if features.get("StudyTimeWeekly", 0) < 10:
        tips.append("Añade 2 sesiones de 1h de estudio enfocado esta semana.")
    if features.get("Absences", 0) > 10:
        tips.append("Baja inasistencias: planifica alarma/recordatorio y pide apuntes.")
    if features.get("Tutoring", 0) == 0:
        tips.append("Agenda tutoría/monitoría 1 vez por semana.")
    if features.get("ParentalSupport", 0) <= 1:
        tips.append("Define 2 metas semanales y compártelas con alguien de apoyo.")
    if features.get("Extracurricular", 0) == 0:
        tips.append("Considera una actividad ligera para balance y motivación.")
    if not tips:
        tips.append("Registra avances diarios y celebra micro-logros.")
    return tips