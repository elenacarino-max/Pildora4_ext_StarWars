from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from components.theme import card, map_node, seals
from core.code_validator import validate_chamber, validate_mission_submission
from core.database import (
    complete_chamber, get_defense, get_mission_runs, get_session, get_team,
    join_team, record_attempt, save_defense, save_mission_run, use_hint,
)
from core.holocrons import holocron_by_id
from core.missions import CHAMBERS, MISSIONS, MISSION_TEMPLATE, chamber_by_index
from core.mlflow_engine import execute_safe_mission


ASSETS = Path(__file__).resolve().parents[1] / "assets"


def _join_panel() -> None:
    st.markdown("## Acceso de equipos")
    left, right = st.columns([1.4, 1])
    with left:
        with st.form("join-team"):
            code = st.text_input("Código de sesión", placeholder="JEDI-4821").upper()
            name = st.text_input("Nombre del equipo", placeholder="Guardianes de Naboo")
            submitted = st.form_submit_button("Entrar en la Biblioteca", use_container_width=True)
        if submitted:
            try:
                team = join_team(code, name)
                st.session_state.team_id = team["id"]
                st.session_state.session_code = code
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
    with right:
        image = ASSETS / "guide-archivist.png"
        if image.exists():
            st.image(str(image), caption="Maestra Sira · Guardiana original del Archivo")
        card("Tres roles, una misión", "Navegante, Escriba y Auditor. Rotad los roles al cambiar de cámara.", "Protocolo de equipo", "gold")


def _sidebar(team: dict, session: dict) -> None:
    with st.sidebar:
        st.markdown("### Expediente del equipo")
        st.write(f"**{team['name']}**")
        st.caption(f"Sesión {session['code']}")
        st.metric("Puntos", team["score"])
        st.metric("Pistas", team["hints_used"])
        seals(min(int(team["chamber_index"]), 6))
        if session.get("global_hint"):
            st.info(f"Mensaje del Consejo: {session['global_hint']}")
        if st.button("Salir del expediente", use_container_width=True):
            st.session_state.pop("team_id", None)
            st.rerun()


def _map(team: dict) -> None:
    st.markdown("## Mapa de la Biblioteca")
    st.caption("Cada término narrativo aparece junto al concepto profesional de MLflow.")
    map_image = ASSETS / "library-map.png"
    if map_image.exists():
        st.image(str(map_image), caption="Seis cámaras conectadas por el Archivo central")
    for index, chamber in enumerate(CHAMBERS):
        if index < team["chamber_index"]:
            state = "done"
        elif index == team["chamber_index"] and team["phase"] == "chambers":
            state = "active"
        else:
            state = "locked"
        map_node(chamber["number"], chamber["title"], chamber["concept"], state)


def _chamber(team: dict) -> None:
    chamber = chamber_by_index(int(team["chamber_index"]))
    if not chamber:
        st.success("Los seis sellos han sido recuperados. El laboratorio está abierto.")
        return
    st.markdown(f"## Cámara {chamber['number']} · {chamber['title']}")
    st.markdown(f'<div class="term-pair"><span>{chamber["title"]}</span><span>{chamber["concept"]}</span></div>', unsafe_allow_html=True)
    st.write(chamber["goal"])
    editor_key = f"chamber-code-{team['id']}-{chamber['id']}"
    code = st.text_area("Terminal de aprendizaje", value=chamber["starter"], height=220, key=editor_key)
    col_validate, col_hint = st.columns([2, 1])
    if col_validate.button("Validar instrucción", type="primary", use_container_width=True):
        result = validate_chamber(chamber["id"], code)
        record_attempt(team["id"], chamber["id"], code, result.valid, result.message)
        if result.valid:
            complete_chamber(team["id"], int(team["chamber_index"]))
            st.success(f"{chamber['seal']} recuperado. +20 puntos")
            st.rerun()
        else:
            st.error(f"Sabotaje detectado: {result.message}")
    hint_level = int(st.session_state.get(f"hint-{chamber['id']}", 0))
    if col_hint.button("Solicitar pista", use_container_width=True, disabled=hint_level >= 3):
        hint_level += 1
        st.session_state[f"hint-{chamber['id']}"] = hint_level
        use_hint(team["id"])
        st.rerun()
    if hint_level:
        st.warning(chamber["hints"][hint_level - 1])


def _mission_editor(team: dict, session: dict) -> None:
    runs = get_mission_runs(team["id"])
    completed = {run["mission_id"] for run in runs}
    st.markdown("## Laboratorio de misiones")
    st.caption("Código Jedi 5–4–2–1: cinco parámetros, cuatro métricas, dos artefactos y un modelo.")
    cols = st.columns(3)
    for col, mission in zip(cols, MISSIONS):
        with col:
            status = "Reconstruida" if mission["id"] in completed else mission["mode"]
            card(mission["title"], mission["brief"], status, "gold" if mission["id"] in completed else "")
    current = next((mission for mission in MISSIONS if mission["id"] not in completed), None)
    if not current:
        st.success("Las tres runs han sido reconstruidas. El comparador está disponible.")
        return
    st.markdown(f"### Mision_{current['title']} · {current['mode']}")
    default = MISSION_TEMPLATE.format(name=current["title"])
    if current["id"] == "coruscant":
        default = default.replace("log_params(parametros)", 'log_metric("n_estimators", 100)').replace("log_metrics(metricas)", 'log_param("accuracy", accuracy)')
    if current["id"] == "mustafar":
        default = "# Registra la misión completa con el Código Jedi 5–4–2–1\n"
    code = st.text_area("Bloque de tracking", value=default, height=330, key=f"mission-{team['id']}-{current['id']}")
    if st.button("Validar y ejecutar plantilla segura", type="primary", use_container_width=True):
        validation = validate_mission_submission(code)
        record_attempt(team["id"], f"mission-{current['id']}", code, validation.valid, validation.message)
        if not validation.valid:
            st.error(validation.message)
            return
        with st.spinner("El Archivo entrena el Random Forest y registra la run real..."):
            try:
                result = execute_safe_mission(session["code"], team["name"], current["id"])
            except RuntimeError as exc:
                st.error(str(exc))
                return
        save_mission_run(team["id"], current["id"], code, result)
        st.success(f"Mision_{current['title']} registrada. Run ID: {result['run_id']}")
        st.rerun()


def _comparator(team: dict) -> None:
    runs = get_mission_runs(team["id"])
    if len(runs) < 3:
        st.info("Reconstruye las tres misiones para abrir el comparador.")
        return
    st.markdown("## Comparador de runs")
    rows = []
    for run in runs:
        mission = next(item for item in MISSIONS if item["id"] == run["mission_id"])
        metrics = run["metrics"]
        rows.append({
            "Run": mission["title"], "Árboles": mission["n_estimators"],
            "Profundidad": mission["max_depth"] or "Sin límite",
            "Accuracy": metrics["accuracy"], "F1 weighted": metrics["f1_weighted"],
            "Recall dígito 1": metrics["recall_1"], "Recall dígito 8": metrics["recall_8"],
        })
    st.dataframe(pd.DataFrame(rows).style.format({"Accuracy":"{:.4f}","F1 weighted":"{:.4f}","Recall dígito 1":"{:.4f}","Recall dígito 8":"{:.4f}"}), use_container_width=True, hide_index=True)
    st.markdown('<div class="status-banner">La accuracy resume. El recall por clase y los artefactos explican dónde están los errores.</div>', unsafe_allow_html=True)


def _defense(team: dict) -> None:
    holocron = holocron_by_id(team.get("holocron_id"))
    if not holocron:
        st.info("Completa las tres runs para recibir el holocrón del Consejo.")
        return
    st.markdown("## Holocrón del Consejo")
    image = ASSETS / "holocron-council.png"
    left, right = st.columns([1, 1.4])
    with left:
        if image.exists():
            st.image(str(image))
        st.markdown(f'<div class="holocron"><div class="holocron-symbol">{holocron["icon"]}</div><h3>{holocron["title"]}</h3><p>{holocron["brief"]}</p></div>', unsafe_allow_html=True)
    with right:
        existing = get_defense(team["id"])
        if existing:
            st.success("Defensa sellada. Utiliza esta tarjeta para la intervención de 45–60 segundos.")
            st.markdown(f"### {team['name']}\n**Run elegida:** {existing['selected_run']}  \n**Evidencia:** {existing['evidence']}  \n**Artefacto:** {existing['artifact']}  \n**Limitación:** {existing['limitation']}  \n**Recomendación:** {existing['recommendation']}")
            return
        with st.form("defense-form"):
            selected = st.selectbox("Run elegida", [item["title"] for item in MISSIONS])
            evidence = st.text_area("Evidencia principal")
            artifact = st.selectbox("Artefacto consultado", ["matriz de confusión", "classification_report.json"])
            discarded = st.selectbox("Run descartada", [item["title"] for item in MISSIONS], index=1)
            reason = st.text_area("Motivo del descarte")
            limitation = st.text_area("Riesgo o limitación")
            recommendation = st.text_area("Recomendación final")
            submit = st.form_submit_button("Sellar defensa", use_container_width=True)
        if submit:
            try:
                save_defense(team["id"], {"selected_run":selected,"evidence":evidence,"artifact":artifact,"discarded_run":discarded,"discard_reason":reason,"limitation":limitation,"recommendation":recommendation})
                st.success("Defensa sellada. +25 puntos")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))


def render_student() -> None:
    if not st.session_state.get("team_id"):
        _join_panel()
        return
    team = get_team(st.session_state.team_id)
    if not team:
        st.session_state.pop("team_id", None)
        st.rerun()
    session = get_session(st.session_state.get("session_code", ""))
    if not session:
        st.error("La sesión ya no está disponible.")
        return
    _sidebar(team, session)
    tabs = st.tabs(["Mapa", "Cámara actual", "Laboratorio", "Comparador", "Consejo"])
    with tabs[0]: _map(team)
    with tabs[1]: _chamber(team)
    with tabs[2]: _mission_editor(team, session)
    with tabs[3]: _comparator(team)
    with tabs[4]: _defense(team)
