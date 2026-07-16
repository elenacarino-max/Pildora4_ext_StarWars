from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from streamlit_ace import st_ace
except ImportError:  # Permite mostrar una ayuda clara si aún no se actualizó el entorno.
    st_ace = None

from components.theme import card, map_node, seals
from core.code_validator import validate_mission_submission, validate_question_answer
from core.database import (
    complete_chamber,
    force_advance_chamber,
    get_defense,
    get_mission_runs,
    get_session,
    get_session_by_id,
    get_team,
    hint_count,
    join_team,
    record_attempt,
    save_defense,
    save_mission_run,
    use_hint,
)
from core.holocrons import holocron_by_id
from core.missions import MISSIONS
from core.mlflow_engine import execute_safe_mission
from core.questions import QUESTION_BY_ID, TEAM_NAMES, questions_from_ids


ASSETS = Path(__file__).resolve().parents[1] / "assets"
MAX_ATTEMPTS = 5


def _leave_game() -> None:
    for key in ("team_id", "session_code", "forced_solution", "mission_selection"):
        st.session_state.pop(key, None)
    st.session_state.portal = "Inicio"
    st.rerun()


def _code_editor(value: str, key: str, height: int = 300) -> str:
    if st_ace is None:
        st.warning("Actualiza las dependencias para activar tabulación avanzada: pip install -r requirements.txt")
        return st.text_area("Código editable", value=value, height=height, key=key)
    result = st_ace(
        value=value,
        language="python",
        theme="twilight",
        key=key,
        height=height,
        font_size=15,
        tab_size=4,
        wrap=True,
        auto_update=True,
        show_gutter=True,
    )
    return result if result is not None else value


def _join_panel() -> None:
    st.markdown("## Acceso de equipos")
    st.caption("La profesora comparte el código. El equipo elige uno de los diez nombres preparados.")
    left, right = st.columns([1.4, 1])
    with left:
        with st.form("join-team"):
            code = st.text_input("Código de sesión", placeholder="JEDI-4821").upper()
            name = st.selectbox("Nombre del equipo", TEAM_NAMES)
            submitted = st.form_submit_button("Entrar en la Biblioteca", use_container_width=True)
        if submitted:
            try:
                team = join_team(code, name)
                st.session_state.team_id = team["id"]
                st.session_state.session_code = code
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
        if st.button("Volver al inicio", use_container_width=True):
            _leave_game()
    with right:
        image = ASSETS / "guide-archivist.png"
        if image.exists():
            st.image(str(image), caption="Maestra Sira · Guardiana original del Archivo")
        card("Expediente ya preparado", "El nombre elegido recibe las seis preguntas de la sesión y las tres misiones. Todo el equipo comparte progreso, pistas y puntuación.", "Protocolo de equipo", "gold")


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
        if st.button("Salir del juego", use_container_width=True, key="sidebar-leave"):
            _leave_game()


def _map(team: dict, session: dict) -> None:
    st.markdown("## Mapa de la Biblioteca")
    st.caption("Las seis cámaras fueron elegidas al azar al crear la sesión, una por cada concepto esencial de MLflow.")
    map_image = ASSETS / "library-map.png"
    if map_image.exists():
        st.image(str(map_image), caption="Seis cámaras conectadas por el Archivo central")
    questions = questions_from_ids(session["question_ids"])
    for index, question in enumerate(questions):
        if index < team["chamber_index"]:
            state = "done"
        elif index == team["chamber_index"] and team["phase"] == "chambers":
            state = "active"
        else:
            state = "locked"
        map_node(index + 1, question["title"], question["topic"], state)


def _forced_solution() -> bool:
    forced = st.session_state.get("forced_solution")
    if not forced:
        return False
    st.error("Se agotaron los cinco intentos. El Archivo abre la compuerta con una penalización de 10 puntos.")
    st.markdown(f"### Solución explicada · {forced['title']}")
    st.write(forced["theory"])
    if forced["kind"] == "code":
        st.code(forced["solution"], language="python")
    else:
        st.success(forced["solution"])
    if st.button("Continuar a la siguiente cámara", type="primary", use_container_width=True):
        st.session_state.pop("forced_solution", None)
        st.rerun()
    return True


def _chamber(team: dict, session: dict) -> None:
    if _forced_solution():
        return
    question_ids = session["question_ids"]
    index = int(team["chamber_index"])
    if index >= len(question_ids):
        st.success("Los seis sellos han sido recuperados. El laboratorio de misiones está abierto.")
        return
    question = QUESTION_BY_ID[question_ids[index]]
    challenge_id = f"question-{question['id']}"
    used_hints = hint_count(team["id"], challenge_id)

    st.markdown(f"## Cámara {index + 1} de 6 · {question['title']}")
    st.markdown(f'<div class="term-pair"><span>Biblioteca Jedi</span><span>{question["topic"]}</span></div>', unsafe_allow_html=True)
    st.info(f"**Archivo teórico:** {question['theory']}")
    st.markdown(f"### Reto\n{question['prompt']}")
    if question.get("context"):
        st.caption("Contexto disponible antes de responder")
        st.code(question["context"], language="python")

    if question["kind"] == "choice":
        answer = st.radio("Elige una respuesta", question["options"], index=None, key=f"answer-{team['id']}-{question['id']}") or ""
    else:
        st.caption("Terminal editable · Tab inserta cuatro espacios · el texto se analiza, nunca se ejecuta")
        answer = _code_editor(question["starter"], f"answer-{team['id']}-{question['id']}", 300)

    left, middle, right = st.columns([2, 1, 1])
    validate = left.button("Validar respuesta", type="primary", use_container_width=True)
    if middle.button("Solicitar pista", use_container_width=True, disabled=used_hints >= 3):
        use_hint(team["id"], challenge_id)
        st.rerun()
    right.metric("Intentos", f"{MAX_ATTEMPTS - min(_invalid_attempts(team['id'], challenge_id), MAX_ATTEMPTS)}/{MAX_ATTEMPTS}")
    if used_hints:
        for hint in question["hints"][:used_hints]:
            st.warning(f"Pista {question['hints'].index(hint) + 1}: {hint}")

    if validate:
        if not answer.strip():
            st.error("Escribe o selecciona una respuesta antes de validar.")
            return
        result = validate_question_answer(question, answer)
        failures = record_attempt(team["id"], challenge_id, answer, result.valid, result.message)
        if result.valid:
            complete_chamber(team["id"], index)
            st.success("Sello recuperado. +20 puntos")
            st.rerun()
        if failures >= MAX_ATTEMPTS:
            force_advance_chamber(team["id"], index)
            st.session_state.forced_solution = question
            st.rerun()
        st.error(f"Sabotaje detectado: {result.message}")
        st.caption(f"Quedan {MAX_ATTEMPTS - failures} intentos. Las pistas cuestan 5 puntos.")


def _invalid_attempts(team_id: str, challenge_id: str) -> int:
    from core.database import attempt_count
    return attempt_count(team_id, challenge_id, valid=False)


def _mission_editor(team: dict, session: dict) -> None:
    if int(team["chamber_index"]) < 6:
        st.info("El laboratorio se abrirá después de completar las seis cámaras. Puedes salir del juego en cualquier momento.")
        return
    runs = get_mission_runs(team["id"])
    completed = {run["mission_id"] for run in runs}
    st.markdown("## Laboratorio de misiones")
    st.caption("Código Jedi 5–4–2–1: cinco parámetros, cuatro métricas, dos artefactos y un modelo.")
    cols = st.columns(3)
    for col, mission in zip(cols, MISSIONS):
        with col:
            status = "Reconstruida" if mission["id"] in completed else mission["mode"]
            card(mission["title"], mission["brief"], status, "gold" if mission["id"] in completed else "")

    next_mission = next((mission for mission in MISSIONS if mission["id"] not in completed), None)
    available = [mission for mission in MISSIONS if mission["id"] in completed]
    if next_mission:
        available.append(next_mission)
    labels = {f"{mission['title']} · {'completada' if mission['id'] in completed else 'disponible'}": mission for mission in available}
    selected_label = st.selectbox("Expediente de misión", labels)
    current = labels[selected_label]

    if current["id"] in completed:
        run = next(item for item in runs if item["mission_id"] == current["id"])
        st.success(f"Mision_{current['title']} ya está registrada. Run ID: {run['run_id']}")
        st.code(run["submitted_code"], language="python")
        return

    st.markdown(f"### Mision_{current['title']} · {current['mode']}")
    st.info(f"**Archivo teórico:** {current['theory']}")
    st.caption("Contexto preparado por scikit-learn; estas variables existen en la plantilla segura")
    st.code(current["context"], language="python")
    st.caption("Terminal editable · usa Tab para indentar · los comentarios con iconos señalan lo que debes completar")
    code = _code_editor(current["starter"], f"mission-{team['id']}-{current['id']}", 390)
    if st.button("Validar y ejecutar misión segura", type="primary", use_container_width=True):
        validation = validate_mission_submission(code, current["id"])
        record_attempt(team["id"], f"mission-{current['id']}", code, validation.valid, validation.message)
        if not validation.valid:
            st.error(validation.message)
            return
        with st.spinner("El Archivo entrena el Random Forest y registra la run real..."):
            try:
                result = execute_safe_mission(session["code"], team["name"], current["id"])
            except Exception as exc:
                st.error(f"La misión no pudo registrarse: {exc}")
                st.info("Tu progreso no se ha perdido. Puedes corregirlo, cambiar de sección o salir del juego.")
                return
        save_mission_run(team["id"], current["id"], code, result)
        st.success(f"Mision_{current['title']} registrada. Run ID: {result['run_id']}")
        st.rerun()


def _comparator(team: dict) -> None:
    runs = get_mission_runs(team["id"])
    if len(runs) < 3:
        st.info(f"Reconstruye las tres misiones para abrir el comparador. Progreso: {len(runs)}/3.")
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
        session = get_session_by_id(team["session_id"])
    if not session:
        st.error("La sesión ya no está disponible.")
        if st.button("Salir del juego", type="primary"):
            _leave_game()
        return

    top_left, top_right = st.columns([5, 1])
    top_left.caption(f"Equipo {team['name']} · sesión {session['code']}")
    if top_right.button("Salir", use_container_width=True, key="top-leave"):
        _leave_game()
    _sidebar(team, session)
    tabs = st.tabs(["Mapa", "Cámara actual", "Laboratorio", "Comparador", "Consejo"])
    with tabs[0]:
        _map(team, session)
    with tabs[1]:
        _chamber(team, session)
    with tabs[2]:
        _mission_editor(team, session)
    with tabs[3]:
        _comparator(team)
    with tabs[4]:
        _defense(team)
