from __future__ import annotations

import os
from pathlib import Path


APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("MLFLOW_JEDI_DATA_DIR", APP_DIR / "data")).resolve()
ARTIFACTS_DIR = DATA_DIR / "artifacts"
GAME_DB = DATA_DIR / "game.db"
MLFLOW_DB = DATA_DIR / "mlflow.db"

TEACHER_PASSWORD = os.getenv("MLFLOW_JEDI_TEACHER_PASSWORD", "1234")
SESSION_PREFIX = "JEDI"
MAX_TEAMS = int(os.getenv("MLFLOW_JEDI_MAX_TEAMS", "7"))


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
