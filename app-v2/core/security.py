from __future__ import annotations

import hmac
import re
import unicodedata


def verify_password(candidate: str, expected: str) -> bool:
    return hmac.compare_digest(candidate.encode("utf-8"), expected.encode("utf-8"))


def safe_slug(value: str, fallback: str = "equipo") -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", normalized).strip("-").lower()
    return slug[:60] or fallback


def clean_team_name(value: str) -> str:
    cleaned = " ".join(value.strip().split())
    if not 2 <= len(cleaned) <= 60:
        raise ValueError("El nombre del equipo debe tener entre 2 y 60 caracteres.")
    if any(char in cleaned for char in "<>\\/"):
        raise ValueError("El nombre contiene caracteres no permitidos.")
    return cleaned
