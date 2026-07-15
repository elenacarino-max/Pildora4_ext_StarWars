from __future__ import annotations

import ast
from dataclasses import dataclass, field


ALLOWED_CALLS = {
    "mlflow.set_experiment", "mlflow.start_run", "mlflow.log_param",
    "mlflow.log_params", "mlflow.log_metric", "mlflow.log_metrics",
    "mlflow.log_artifact", "mlflow.sklearn.log_model",
}


@dataclass
class ValidationResult:
    valid: bool
    message: str
    calls: list[str] = field(default_factory=list)


def _call_name(node: ast.Call) -> str:
    parts: list[str] = []
    current: ast.AST = node.func
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


def _parse_safe(code: str) -> tuple[ast.Module | None, ValidationResult | None]:
    if len(code) > 12_000:
        return None, ValidationResult(False, "El fragmento es demasiado largo para esta cámara.")
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        return None, ValidationResult(False, f"Error de sintaxis en la línea {exc.lineno}: {exc.msg}.")

    forbidden = (ast.Import, ast.ImportFrom, ast.Lambda, ast.Global, ast.Nonlocal)
    if any(isinstance(node, forbidden) for node in ast.walk(tree)):
        return None, ValidationResult(False, "El Archivo solo acepta instrucciones de tracking.")

    calls = [_call_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    unsafe = [call for call in calls if call and call not in ALLOWED_CALLS]
    if unsafe:
        return None, ValidationResult(False, f"{unsafe[0]} no está autorizada en esta terminal.", calls)
    return tree, None


def validate_chamber(chamber_id: str, code: str) -> ValidationResult:
    tree, error = _parse_safe(code)
    if error:
        return error
    assert tree is not None
    calls = [(_call_name(node), node) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    names = [name for name, _ in calls]
    expected = {
        "experiment": "mlflow.set_experiment", "run": "mlflow.start_run",
        "parameters": "mlflow.log_params", "metrics": "mlflow.log_metrics",
        "artifacts": "mlflow.log_artifact", "model": "mlflow.sklearn.log_model",
    }[chamber_id]
    if expected not in names:
        feedback = {
            "experiment": "Primero selecciona la campaña que agrupará las ejecuciones.",
            "run": "Necesitamos una run delimitada para una ejecución concreta.",
            "parameters": "n_estimators y max_depth son decisiones previas: son parámetros.",
            "metrics": "La accuracy se conoce después de evaluar: es una métrica.",
            "artifacts": "Una matriz de confusión es un archivo, no una cifra única.",
            "model": "Registrar resultados no conserva el modelo entrenado.",
        }[chamber_id]
        return ValidationResult(False, feedback, names)
    if chamber_id == "run" and not any(isinstance(node, ast.With) for node in ast.walk(tree)):
        return ValidationResult(False, "Abre la run dentro de un bloque with.", names)
    if chamber_id == "experiment":
        node = next(node for name, node in calls if name == expected)
        if not node.args or not isinstance(node.args[0], ast.Constant) or node.args[0].value != "Biblioteca_Jedi_Digits":
            return ValidationResult(False, "Usa exactamente Biblioteca_Jedi_Digits.", names)
    if chamber_id == "model":
        node = next(node for name, node in calls if name == expected)
        keywords = {kw.arg: kw.value for kw in node.keywords if kw.arg}
        if "sk_model" not in keywords or "artifact_path" not in keywords:
            return ValidationResult(False, "Indica sk_model=modelo y artifact_path=\"modelo_digits\".", names)
    return ValidationResult(True, "Sello recuperado. El Archivo reconoce el concepto.", names)


def validate_mission_submission(code: str) -> ValidationResult:
    tree, error = _parse_safe(code)
    if error:
        return error
    assert tree is not None
    names = [_call_name(node) for node in ast.walk(tree) if isinstance(node, ast.Call)]
    required = {"mlflow.start_run", "mlflow.log_params", "mlflow.log_metrics",
                "mlflow.log_artifact", "mlflow.sklearn.log_model"}
    missing = sorted(required.difference(names))
    if missing:
        return ValidationResult(False, "Faltan piezas del Código Jedi 5–4–2–1: " + ", ".join(missing), names)
    if names.count("mlflow.log_artifact") < 2:
        return ValidationResult(False, "La misión necesita dos artefactos de evidencia.", names)
    return ValidationResult(True, "Tracking validado. La plantilla segura puede ejecutar la misión.", names)
