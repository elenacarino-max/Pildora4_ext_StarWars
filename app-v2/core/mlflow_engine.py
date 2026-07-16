from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

from .config import ARTIFACTS_DIR, DATA_DIR, MLFLOW_DB, ensure_data_dirs
from .missions import ORIENTATIVE_RESULTS, mission_by_id
from .security import safe_slug


def execute_safe_mission(session_code: str, team_name: str, mission_id: str) -> dict:
    """Entrena una plantilla propia. Nunca ejecuta el texto enviado por el alumnado."""
    ensure_data_dirs()
    # MLflow usa ./mlruns como raíz inicial al abrir un backend SQL. Situamos
    # ese directorio dentro del volumen persistente antes de crear el cliente.
    os.chdir(DATA_DIR)
    mpl_config = DATA_DIR / ".matplotlib"
    mpl_config.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(mpl_config))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import mlflow
        import mlflow.sklearn
        from mlflow.models import infer_signature
        from mlflow.tracking import MlflowClient
        from sklearn.datasets import load_digits
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.metrics import (
            ConfusionMatrixDisplay,
            accuracy_score,
            classification_report,
            f1_score,
            precision_score,
            recall_score,
        )
        from sklearn.model_selection import train_test_split
    except ImportError as exc:
        raise RuntimeError(
            "Faltan dependencias de ML: instala requirements.txt antes de ejecutar misiones reales."
        ) from exc

    mission = mission_by_id(mission_id)
    digits = load_digits()
    x_train, x_test, y_train, y_test = train_test_split(
        digits.data,
        digits.target,
        test_size=0.20,
        random_state=42,
        stratify=digits.target,
    )
    model = RandomForestClassifier(
        n_estimators=mission["n_estimators"],
        max_depth=mission["max_depth"],
        random_state=42,
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision_weighted": precision_score(y_test, predictions, average="weighted", zero_division=0),
        "recall_weighted": recall_score(y_test, predictions, average="weighted", zero_division=0),
        "f1_weighted": f1_score(y_test, predictions, average="weighted", zero_division=0),
        "recall_1": report["1"]["recall"],
        "recall_8": report["8"]["recall"],
    }
    params = {
        "dataset": "digits",
        "n_estimators": mission["n_estimators"],
        "max_depth": "None" if mission["max_depth"] is None else mission["max_depth"],
        "test_size": 0.20,
        "random_state": 42,
    }

    run_folder = ARTIFACTS_DIR / safe_slug(session_code) / safe_slug(team_name) / mission_id / str(uuid.uuid4())
    run_folder.mkdir(parents=True, exist_ok=True)
    matrix_path = run_folder / "matriz_confusion.png"
    report_path = run_folder / "classification_report.json"
    ConfusionMatrixDisplay.from_predictions(y_test, predictions, display_labels=digits.target_names, cmap="Blues")
    plt.title(f"Matriz de confusión · Mision_{mission['title']}")
    plt.tight_layout()
    plt.savefig(matrix_path, dpi=150)
    plt.close()
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    tracking_uri = f"sqlite:///{MLFLOW_DB.as_posix()}"
    mlflow.set_tracking_uri(tracking_uri)
    experiment_name = f"Biblioteca_Jedi_Digits_{safe_slug(session_code)}"
    client = MlflowClient(tracking_uri=tracking_uri)
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        artifact_root = ARTIFACTS_DIR / "mlflow"
        artifact_root.mkdir(parents=True, exist_ok=True)
        experiment_id = client.create_experiment(experiment_name, artifact_location=artifact_root.as_uri())
    else:
        experiment_id = experiment.experiment_id
    mlflow.set_experiment(experiment_id=experiment_id)
    with mlflow.start_run(run_name=f"Mision_{mission['title']}") as run:
        mlflow.set_tags({"equipo": team_name, "sesion": session_code, "universo": "Biblioteca Jedi"})
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(str(matrix_path), artifact_path="evidencias")
        mlflow.log_artifact(str(report_path), artifact_path="evidencias")
        signature = infer_signature(x_train, model.predict(x_train))
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="modelo_digits",
            signature=signature,
            input_example=x_train[:3],
        )
        run_id = run.info.run_id

    return {"run_id": run_id, "params": params, **metrics,
            "matrix_path": str(matrix_path), "report_path": str(report_path)}


def demo_result(mission_id: str) -> dict:
    """Resultados de contingencia claramente marcados; no crean una run real."""
    return {"run_id": f"demo-{mission_id}", "demo": True, **ORIENTATIVE_RESULTS[mission_id]}
