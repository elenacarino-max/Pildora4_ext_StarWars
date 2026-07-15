from __future__ import annotations

import pandas as pd
import streamlit as st

from core.config import TEACHER_PASSWORD
from core.database import (
    create_session, delete_session, export_session, get_defense, get_session,
    list_sessions, list_teams, reassign_holocron, reset_team, set_global_hint,
    set_session_status, unlock_next_chamber,
)
from core.holocrons import HOLOCRONS, holocron_by_id
from core.security import verify_password


def _login() -> bool:
    if st.session_state.get("teacher_authenticated"):
        return True
    st.markdown("## Acceso del profesorado")
    st.caption("La contraseña se configura mediante una variable de entorno y no se guarda en la interfaz.")
    with st.form("teacher-login"):
        password = st.text_input("Contraseña docente", type="password")
        submitted = st.form_submit_button("Abrir panel", use_container_width=True)
    if submitted:
        if verify_password(password, TEACHER_PASSWORD):
            st.session_state.teacher_authenticated = True
            st.rerun()
        st.error("Contraseña incorrecta.")
    return False


def _session_selector() -> dict | None:
    sessions = list_sessions()
    top_left, top_right = st.columns([2, 1])
    with top_left:
        st.markdown("## Centro de mando del Consejo")
        st.caption("Crea una sesión, comparte el código y acompaña el progreso sin ejecutar código del alumnado.")
    with top_right:
        if st.button("Crear nueva sesión", type="primary", use_container_width=True):
            session = create_session()
            st.session_state.selected_session_code = session["code"]
            st.rerun()
    if not sessions:
        st.info("Todavía no hay sesiones. Crea la primera para obtener un código de acceso.")
        return None
    codes = [session["code"] for session in sessions]
    default = st.session_state.get("selected_session_code", codes[0])
    index = codes.index(default) if default in codes else 0
    code = st.selectbox("Sesión activa en el panel", codes, index=index)
    st.session_state.selected_session_code = code
    return get_session(code)


def _session_controls(session: dict) -> None:
    st.markdown(f"### Código para equipos: `{session['code']}`")
    a, b, c = st.columns(3)
    a.metric("Estado", "Abierta" if session["status"] == "open" else "Cerrada")
    if b.button("Cerrar sesión" if session["status"] == "open" else "Reabrir sesión", use_container_width=True):
        set_session_status(session["id"], "closed" if session["status"] == "open" else "open")
        st.rerun()
    if c.button("Salir del panel", use_container_width=True):
        st.session_state.teacher_authenticated = False
        st.rerun()
    with st.form("global-hint"):
        hint = st.text_input("Pista o aviso global", value=session.get("global_hint", ""), placeholder="Revisad si el dato se conoce antes o después de entrenar")
        if st.form_submit_button("Enviar al Archivo"):
            set_global_hint(session["id"], hint)
            st.success("Mensaje actualizado.")


def _team_table(session: dict) -> list[dict]:
    teams = list_teams(session["id"])
    st.markdown("### Seguimiento de equipos")
    if not teams:
        st.info("Aún no se ha conectado ningún equipo.")
        return []
    data = []
    for team in teams:
        holo = holocron_by_id(team.get("holocron_id"))
        data.append({
            "Equipo": team["name"], "Estado": team["phase"],
            "Cámara": f"{min(team['chamber_index'], 6)}/6",
            "Misiones": f"{team['missions_completed']}/3", "Intentos": team["attempts"],
            "Pistas": team["hints_used"], "Puntos": team["score"],
            "Holocrón": holo["title"] if holo else "—",
        })
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    return teams


def _interventions(teams: list[dict]) -> None:
    if not teams:
        return
    st.markdown("### Intervenciones del Consejo")
    names = {team["name"]: team for team in teams}
    selected_name = st.selectbox("Equipo", list(names))
    team = names[selected_name]
    left, middle, right = st.columns(3)
    if left.button("Desbloquear siguiente", use_container_width=True):
        unlock_next_chamber(team["id"])
        st.success("Progreso actualizado.")
        st.rerun()
    holo_titles = {item["title"]: item["id"] for item in HOLOCRONS}
    chosen_title = middle.selectbox("Reasignar holocrón", list(holo_titles), label_visibility="collapsed")
    if middle.button("Asignar holocrón", use_container_width=True):
        reassign_holocron(team["id"], holo_titles[chosen_title])
        st.rerun()
    confirm = right.checkbox("Confirmar reinicio", key=f"confirm-{team['id']}")
    if right.button("Reiniciar equipo", use_container_width=True, disabled=not confirm):
        reset_team(team["id"])
        st.rerun()


def _defenses(teams: list[dict]) -> None:
    st.markdown("### Defensas selladas")
    found = False
    for team in teams:
        defense = get_defense(team["id"])
        if not defense:
            continue
        found = True
        with st.expander(f"{team['name']} · {defense['selected_run']}"):
            st.write(f"**Evidencia:** {defense['evidence']}")
            st.write(f"**Artefacto:** {defense['artifact']}")
            st.write(f"**Run descartada:** {defense['discarded_run']} — {defense['discard_reason']}")
            st.write(f"**Limitación:** {defense['limitation']}")
            st.info(defense["recommendation"])
    if not found:
        st.caption("Todavía no hay defensas completas.")


def _exports(session: dict) -> None:
    st.markdown("### Copias de seguridad y exportación")
    left, right = st.columns(2)
    left.download_button("Descargar JSON completo", export_session(session["id"], "json"), file_name=f"{session['code']}-resultados.json", mime="application/json", use_container_width=True)
    right.download_button("Descargar resumen CSV", export_session(session["id"], "csv"), file_name=f"{session['code']}-resumen.csv", mime="text/csv", use_container_width=True)
    with st.expander("Zona de pruebas: borrar sesión"):
        confirm = st.checkbox("Entiendo que se eliminarán equipos, intentos y defensas", key="delete-confirm")
        if st.button("Borrar esta sesión", disabled=not confirm):
            delete_session(session["id"])
            st.session_state.pop("selected_session_code", None)
            st.rerun()


def render_teacher() -> None:
    if not _login():
        return
    session = _session_selector()
    if not session:
        return
    _session_controls(session)
    teams = _team_table(session)
    _interventions(teams)
    _defenses(teams)
    _exports(session)
