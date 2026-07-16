from __future__ import annotations

import streamlit as st

from components.theme import apply_theme, card, hero
from core.database import init_db
from views.student import render_student
from views.teacher import render_teacher


st.set_page_config(
    page_title="MLflow Jedi · Cámara de los Experimentos Perdidos",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
init_db()
apply_theme()


def home() -> None:
    hero()
    st.markdown("## El protocolo de recuperación")
    one, two, three = st.columns(3)
    with one:
        card("Comprender las piezas", "Recupera seis sellos relacionando Biblioteca, Misión, Estrategia, Consejo, Holocrón y Jedi entrenado con el vocabulario real de MLflow.", "Fase 01")
    with two:
        card("Registrar experimentos", "Reconstruye Tatooine, Coruscant y Mustafar. Tu código se analiza de forma segura y una plantilla interna registra las runs.", "Fase 02", "gold")
    with three:
        card("Defender una decisión", "Compara métricas y artefactos, recibe un holocrón y presenta una recomendación con evidencia y limitaciones.", "Fase 03")
    st.markdown("### Acceso rápido")
    left, right = st.columns(2)
    if left.button("Soy un equipo", type="primary", use_container_width=True):
        st.session_state.portal = "Alumnado"
        st.rerun()
    if right.button("Soy profesora", use_container_width=True):
        st.session_state.portal = "Profesorado"
        st.rerun()


portal = st.sidebar.radio(
    "Portal",
    ["Inicio", "Alumnado", "Profesorado"],
    index=["Inicio", "Alumnado", "Profesorado"].index(st.session_state.get("portal", "Inicio")),
)
st.session_state.portal = portal

if portal == "Inicio":
    home()
elif portal == "Alumnado":
    render_student()
else:
    render_teacher()
