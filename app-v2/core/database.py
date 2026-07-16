from __future__ import annotations

import csv
import io
import json
import secrets
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from .config import GAME_DB, MAX_TEAMS, SESSION_PREFIX, ensure_data_dirs
from .holocrons import HOLOCRONS
from .questions import TEAM_NAMES, choose_session_question_ids
from .security import clean_team_name


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@contextmanager
def connect():
    ensure_data_dirs()
    connection = sqlite3.connect(GAME_DB, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute("PRAGMA journal_mode=WAL")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db() -> None:
    with connect() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY, code TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open',
                global_hint TEXT NOT NULL DEFAULT '', scoreboard_visible INTEGER NOT NULL DEFAULT 0,
                question_ids_json TEXT NOT NULL DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY, session_id TEXT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                name TEXT NOT NULL, joined_at TEXT NOT NULL,
                chamber_index INTEGER NOT NULL DEFAULT 0, phase TEXT NOT NULL DEFAULT 'chambers',
                score INTEGER NOT NULL DEFAULT 0, hints_used INTEGER NOT NULL DEFAULT 0,
                holocron_id TEXT, UNIQUE(session_id, name)
            );
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, team_id TEXT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
                challenge_id TEXT NOT NULL, submitted_code TEXT NOT NULL,
                valid INTEGER NOT NULL, feedback TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS hint_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id TEXT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
                challenge_id TEXT NOT NULL, level INTEGER NOT NULL, used_at TEXT NOT NULL,
                UNIQUE(team_id, challenge_id, level)
            );
            CREATE TABLE IF NOT EXISTS mission_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, team_id TEXT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
                mission_id TEXT NOT NULL, run_id TEXT, submitted_code TEXT NOT NULL,
                metrics_json TEXT NOT NULL, completed_at TEXT NOT NULL,
                UNIQUE(team_id, mission_id)
            );
            CREATE TABLE IF NOT EXISTS defenses (
                team_id TEXT PRIMARY KEY REFERENCES teams(id) ON DELETE CASCADE,
                selected_run TEXT NOT NULL, evidence TEXT NOT NULL, artifact TEXT NOT NULL,
                discarded_run TEXT NOT NULL, discard_reason TEXT NOT NULL,
                limitation TEXT NOT NULL, recommendation TEXT NOT NULL, sealed_at TEXT NOT NULL
            );
            """
        )
        columns = {row[1] for row in db.execute("PRAGMA table_info(sessions)")}
        if "question_ids_json" not in columns:
            db.execute("ALTER TABLE sessions ADD COLUMN question_ids_json TEXT NOT NULL DEFAULT '[]'")


def _row(row: sqlite3.Row | None) -> dict | None:
    return dict(row) if row else None


def _session_row(row: sqlite3.Row | None) -> dict | None:
    session = _row(row)
    if not session:
        return None
    try:
        question_ids = json.loads(session.get("question_ids_json") or "[]")
    except json.JSONDecodeError:
        question_ids = []
    if len(question_ids) != 6:
        question_ids = choose_session_question_ids()
        with connect() as db:
            db.execute(
                "UPDATE sessions SET question_ids_json=? WHERE id=?",
                (json.dumps(question_ids), session["id"]),
            )
    session["question_ids"] = question_ids
    return session


def create_session() -> dict:
    init_db()
    for _ in range(20):
        code = f"{SESSION_PREFIX}-{secrets.randbelow(9000) + 1000}"
        session = {
            "id": str(uuid.uuid4()),
            "code": code,
            "created_at": _now(),
            "question_ids_json": json.dumps(choose_session_question_ids()),
        }
        try:
            with connect() as db:
                db.execute(
                    """INSERT INTO sessions(id, code, created_at, question_ids_json)
                       VALUES (:id, :code, :created_at, :question_ids_json)""",
                    session,
                )
            return get_session(code) or session
        except sqlite3.IntegrityError:
            continue
    raise RuntimeError("No se pudo generar un código de sesión único.")


def get_session(code: str) -> dict | None:
    with connect() as db:
        row = db.execute("SELECT * FROM sessions WHERE code=?", (code.strip().upper(),)).fetchone()
    return _session_row(row)


def get_session_by_id(session_id: str) -> dict | None:
    with connect() as db:
        row = db.execute("SELECT * FROM sessions WHERE id=?", (session_id,)).fetchone()
    return _session_row(row)


def list_sessions() -> list[dict]:
    with connect() as db:
        rows = db.execute("SELECT * FROM sessions ORDER BY created_at DESC").fetchall()
    return [_session_row(row) for row in rows]


def set_session_status(session_id: str, status: str) -> None:
    if status not in {"open", "closed"}:
        raise ValueError("Estado no válido")
    with connect() as db:
        db.execute("UPDATE sessions SET status=? WHERE id=?", (status, session_id))


def set_global_hint(session_id: str, hint: str) -> None:
    with connect() as db:
        db.execute("UPDATE sessions SET global_hint=? WHERE id=?", (hint.strip()[:500], session_id))


def join_team(session_code: str, team_name: str) -> dict:
    session = get_session(session_code)
    if not session or session["status"] != "open":
        raise ValueError("La sesión no existe o está cerrada.")
    name = clean_team_name(team_name)
    if name not in TEAM_NAMES:
        raise ValueError("Selecciona uno de los nombres de equipo disponibles.")
    with connect() as db:
        existing = db.execute(
            "SELECT * FROM teams WHERE session_id=? AND name=?", (session["id"], name)
        ).fetchone()
        if existing:
            return dict(existing)
        count = db.execute("SELECT COUNT(*) FROM teams WHERE session_id=?", (session["id"],)).fetchone()[0]
        if count >= MAX_TEAMS:
            raise ValueError("La sesión ya tiene el máximo de equipos.")
        team = {"id": str(uuid.uuid4()), "session_id": session["id"], "name": name, "joined_at": _now()}
        db.execute(
            "INSERT INTO teams(id, session_id, name, joined_at) VALUES (:id,:session_id,:name,:joined_at)",
            team,
        )
    return get_team(team["id"]) or team


def get_team(team_id: str) -> dict | None:
    with connect() as db:
        return _row(db.execute("SELECT * FROM teams WHERE id=?", (team_id,)).fetchone())


def list_teams(session_id: str) -> list[dict]:
    with connect() as db:
        query = """
            SELECT t.*, COUNT(DISTINCT mr.mission_id) AS missions_completed,
                   COUNT(a.id) AS attempts
            FROM teams t
            LEFT JOIN mission_runs mr ON mr.team_id=t.id
            LEFT JOIN attempts a ON a.team_id=t.id
            WHERE t.session_id=? GROUP BY t.id ORDER BY t.joined_at
        """
        return [dict(row) for row in db.execute(query, (session_id,))]


def record_attempt(team_id: str, challenge_id: str, code: str, valid: bool, feedback: str) -> int:
    with connect() as db:
        db.execute(
            "INSERT INTO attempts(team_id,challenge_id,submitted_code,valid,feedback,created_at) VALUES (?,?,?,?,?,?)",
            (team_id, challenge_id, code[:12000], int(valid), feedback[:1000], _now()),
        )
        return db.execute(
            "SELECT COUNT(*) FROM attempts WHERE team_id=? AND challenge_id=? AND valid=0",
            (team_id, challenge_id),
        ).fetchone()[0]


def attempt_count(team_id: str, challenge_id: str, valid: bool | None = None) -> int:
    query = "SELECT COUNT(*) FROM attempts WHERE team_id=? AND challenge_id=?"
    values: list[object] = [team_id, challenge_id]
    if valid is not None:
        query += " AND valid=?"
        values.append(int(valid))
    with connect() as db:
        return db.execute(query, values).fetchone()[0]


def hint_count(team_id: str, challenge_id: str) -> int:
    with connect() as db:
        return db.execute(
            "SELECT COUNT(*) FROM hint_usage WHERE team_id=? AND challenge_id=?",
            (team_id, challenge_id),
        ).fetchone()[0]


def use_hint(team_id: str, challenge_id: str) -> int:
    with connect() as db:
        level = db.execute(
            "SELECT COUNT(*) FROM hint_usage WHERE team_id=? AND challenge_id=?",
            (team_id, challenge_id),
        ).fetchone()[0]
        if level >= 3:
            return level
        level += 1
        db.execute(
            "INSERT OR IGNORE INTO hint_usage(team_id,challenge_id,level,used_at) VALUES (?,?,?,?)",
            (team_id, challenge_id, level, _now()),
        )
        db.execute(
            "UPDATE teams SET hints_used=hints_used+1, score=score-5 WHERE id=?",
            (team_id,),
        )
        return level


def complete_chamber(team_id: str, chamber_index: int) -> dict:
    with connect() as db:
        team = db.execute("SELECT chamber_index FROM teams WHERE id=?", (team_id,)).fetchone()
        if not team:
            raise ValueError("Equipo no encontrado")
        if team[0] == chamber_index:
            next_index = chamber_index + 1
            phase = "missions" if next_index >= 6 else "chambers"
            db.execute(
                "UPDATE teams SET chamber_index=?, phase=?, score=score+20 WHERE id=?",
                (next_index, phase, team_id),
            )
    return get_team(team_id) or {}


def force_advance_chamber(team_id: str, chamber_index: int) -> dict:
    """Evita bloqueos tras cinco fallos y aplica la penalización acordada."""
    with connect() as db:
        team = db.execute("SELECT chamber_index FROM teams WHERE id=?", (team_id,)).fetchone()
        if not team:
            raise ValueError("Equipo no encontrado")
        if team[0] == chamber_index:
            next_index = chamber_index + 1
            phase = "missions" if next_index >= 6 else "chambers"
            db.execute(
                "UPDATE teams SET chamber_index=?, phase=?, score=score-10 WHERE id=?",
                (next_index, phase, team_id),
            )
    return get_team(team_id) or {}


def save_mission_run(team_id: str, mission_id: str, submitted_code: str, result: dict) -> dict:
    with connect() as db:
        exists = db.execute(
            "SELECT id FROM mission_runs WHERE team_id=? AND mission_id=?", (team_id, mission_id)
        ).fetchone()
        if not exists:
            db.execute(
                "INSERT INTO mission_runs(team_id,mission_id,run_id,submitted_code,metrics_json,completed_at) VALUES (?,?,?,?,?,?)",
                (team_id, mission_id, result.get("run_id"), submitted_code, json.dumps(result), _now()),
            )
            db.execute("UPDATE teams SET score=score+30 WHERE id=?", (team_id,))
        completed = db.execute("SELECT COUNT(*) FROM mission_runs WHERE team_id=?", (team_id,)).fetchone()[0]
        if completed >= 3:
            db.execute("UPDATE teams SET phase='comparator', score=score+15 WHERE id=? AND phase='missions'", (team_id,))
    assign_holocron(team_id)
    return get_team(team_id) or {}


def get_mission_runs(team_id: str) -> list[dict]:
    with connect() as db:
        rows = db.execute("SELECT * FROM mission_runs WHERE team_id=? ORDER BY id", (team_id,)).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["metrics"] = json.loads(item.pop("metrics_json"))
        result.append(item)
    return result


def assign_holocron(team_id: str, holocron_id: str | None = None) -> str | None:
    team = get_team(team_id)
    if not team or team.get("holocron_id"):
        return team.get("holocron_id") if team else None
    runs = get_mission_runs(team_id)
    if len(runs) < 3:
        return None
    with connect() as db:
        position = db.execute(
            "SELECT COUNT(*) FROM teams WHERE session_id=? AND joined_at<=?",
            (team["session_id"], team["joined_at"]),
        ).fetchone()[0]
        chosen = holocron_id or HOLOCRONS[(position - 1) % len(HOLOCRONS)]["id"]
        db.execute("UPDATE teams SET holocron_id=?, phase='defense' WHERE id=?", (chosen, team_id))
    return chosen


def reassign_holocron(team_id: str, holocron_id: str) -> None:
    if holocron_id not in {item["id"] for item in HOLOCRONS}:
        raise ValueError("Holocrón no válido")
    with connect() as db:
        db.execute("UPDATE teams SET holocron_id=? WHERE id=?", (holocron_id, team_id))


def save_defense(team_id: str, payload: dict) -> None:
    required = ["selected_run", "evidence", "artifact", "discarded_run", "discard_reason", "limitation", "recommendation"]
    if any(not str(payload.get(key, "")).strip() for key in required):
        raise ValueError("Completa todos los campos antes de sellar la defensa.")
    if payload["selected_run"] == payload["discarded_run"]:
        raise ValueError("La run elegida y la descartada deben ser distintas.")
    values = [str(payload[key]).strip() for key in required]
    with connect() as db:
        exists = db.execute("SELECT team_id FROM defenses WHERE team_id=?", (team_id,)).fetchone()
        db.execute(
            """INSERT OR REPLACE INTO defenses
               (team_id,selected_run,evidence,artifact,discarded_run,discard_reason,limitation,recommendation,sealed_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (team_id, *values, _now()),
        )
        if not exists:
            db.execute("UPDATE teams SET phase='completed', score=score+25 WHERE id=?", (team_id,))


def get_defense(team_id: str) -> dict | None:
    with connect() as db:
        return _row(db.execute("SELECT * FROM defenses WHERE team_id=?", (team_id,)).fetchone())


def reset_team(team_id: str) -> None:
    with connect() as db:
        db.execute("DELETE FROM attempts WHERE team_id=?", (team_id,))
        db.execute("DELETE FROM hint_usage WHERE team_id=?", (team_id,))
        db.execute("DELETE FROM mission_runs WHERE team_id=?", (team_id,))
        db.execute("DELETE FROM defenses WHERE team_id=?", (team_id,))
        db.execute("UPDATE teams SET chamber_index=0,phase='chambers',score=0,hints_used=0,holocron_id=NULL WHERE id=?", (team_id,))


def unlock_next_chamber(team_id: str) -> None:
    team = get_team(team_id)
    if team and team["phase"] == "chambers":
        complete_chamber(team_id, int(team["chamber_index"]))


def export_session(session_id: str, format: str = "json") -> bytes:
    teams = list_teams(session_id)
    payload = []
    for team in teams:
        team["runs"] = get_mission_runs(team["id"])
        team["defense"] = get_defense(team["id"])
        payload.append(team)
    if format == "json":
        return json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    output = io.StringIO()
    fields = ["name", "phase", "chamber_index", "missions_completed", "score", "hints_used", "holocron_id"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows({key: team.get(key) for key in fields} for team in payload)
    return output.getvalue().encode("utf-8-sig")


def delete_session(session_id: str) -> None:
    with connect() as db:
        db.execute("DELETE FROM sessions WHERE id=?", (session_id,))
