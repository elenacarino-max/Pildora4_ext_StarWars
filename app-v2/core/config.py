from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


APP_DIR = Path(__file__).resolve().parents[1]
load_dotenv(APP_DIR / ".env")
_configured_data_dir = Path(os.getenv("MLFLOW_JEDI_DATA_DIR", "data"))
DATA_DIR = (
    _configured_data_dir if _configured_data_dir.is_absolute()
    else APP_DIR / _configured_data_dir
).resolve()
ARTIFACTS_DIR = DATA_DIR / "artifacts"
GAME_DB = DATA_DIR / "game.db"
MLFLOW_DB = DATA_DIR / "mlflow.db"

TEACHER_PASSWORD = os.getenv("MLFLOW_JEDI_TEACHER_PASSWORD", "1234")
SESSION_PREFIX = "JEDI"
MAX_TEAMS = int(os.getenv("MLFLOW_JEDI_MAX_TEAMS", "10"))


def ensure_data_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
