from __future__ import annotations


CHAMBERS = [
    {
        "id": "experiment",
        "number": 1,
        "title": "Archivo de campañas",
        "concept": "Experiment",
        "seal": "Sello de la Biblioteca",
        "goal": "Selecciona la campaña que agrupará todas las ejecuciones.",
        "starter": 'mlflow.set_experiment("Biblioteca_Jedi_Digits")',
        "hints": [
            "Una campaña agrupa runs relacionadas.",
            "La función pertenece a la categoría Experiment.",
            'mlflow.set_e_________("Biblioteca_Jedi_Digits")',
        ],
    },
    {
        "id": "run",
        "number": 2,
        "title": "Cámara de las misiones",
        "concept": "Run",
        "seal": "Sello de la Misión",
        "goal": "Abre una ejecución llamada Mision_Coruscant y delimítala con with.",
        "starter": 'with mlflow.start_run(run_name="Mision_Coruscant"):\n    pass',
        "hints": [
            "Cada entrenamiento concreto necesita su propia run.",
            "Usa start_run dentro de un bloque with.",
            'with mlflow.start_r__(run_name="Mision_Coruscant"):',
        ],
    },
    {
        "id": "parameters",
        "number": 3,
        "title": "Sala de estrategias",
        "concept": "Parameters",
        "seal": "Sello de la Estrategia",
        "goal": "Registra el diccionario parametros como decisiones previas.",
        "starter": "parametros = {\n    \"n_estimators\": 100,\n    \"max_depth\": 10,\n    \"random_state\": 42,\n}\n\n# Escribe aquí el registro",
        "hints": [
            "Estos datos se conocen antes de entrenar.",
            "Deben registrarse como parámetros.",
            "mlflow.log_p____(parametros)",
        ],
    },
    {
        "id": "metrics",
        "number": 4,
        "title": "Consejo de evaluación",
        "concept": "Metrics",
        "seal": "Sello del Consejo",
        "goal": "Registra el diccionario metricas como resultados de evaluación.",
        "starter": "metricas = {\n    \"accuracy\": accuracy,\n    \"precision_weighted\": precision_weighted,\n    \"recall_weighted\": recall_weighted,\n    \"f1_weighted\": f1_weighted,\n}\n\n# Escribe aquí el registro",
        "hints": [
            "Estas cifras se conocen después de evaluar.",
            "No son configuración: son métricas.",
            "mlflow.log_m______(metricas)",
        ],
    },
    {
        "id": "artifacts",
        "number": 5,
        "title": "Cámara de holocrones",
        "concept": "Artifacts",
        "seal": "Sello del Holocrón",
        "goal": "Registra matriz_confusion.png como archivo de evidencia.",
        "starter": 'archivo = "matriz_confusion.png"\n\n# Escribe aquí el registro',
        "hints": [
            "Una imagen no es una cifra única.",
            "Debe guardarse como artefacto.",
            "mlflow.log_a_______(archivo)",
        ],
    },
    {
        "id": "model",
        "number": 6,
        "title": "Archivo de modelos",
        "concept": "Model",
        "seal": "Sello del Jedi entrenado",
        "goal": "Conserva el modelo entrenado bajo modelo_digits.",
        "starter": "mlflow.sklearn.log_model(\n    sk_model=modelo,\n    artifact_path=\"modelo_digits\",\n)",
        "hints": [
            "Las métricas no guardan el objeto entrenado.",
            "Usa la integración mlflow.sklearn.",
            "mlflow.sklearn.log_m____(sk_model=modelo, ...)",
        ],
    },
]


MISSIONS = [
    {
        "id": "tatooine",
        "title": "Tatooine",
        "mode": "Misión guiada",
        "n_estimators": 50,
        "max_depth": 8,
        "accent": "#d9a441",
        "brief": "Completa una estructura preparada y recupera el primer expediente.",
        "theory": "Una run reúne la configuración usada, los resultados obtenidos, los archivos de diagnóstico y el modelo. Aquí practicarás el patrón completo sin ejecutar tu texto: la app valida su estructura y después utiliza una plantilla interna segura.",
        "context": """parametros = {\"dataset\": \"digits\", \"n_estimators\": 50, \"max_depth\": 8, \"test_size\": 0.2, \"random_state\": 42}\nmetricas = {\"accuracy\": accuracy, \"precision_weighted\": precision_weighted, \"recall_weighted\": recall_weighted, \"f1_weighted\": f1_weighted}\n# También existen modelo, matriz_confusion.png y classification_report.json""",
        "starter": """# 🛰️ MISIÓN GUIADA: completa las cinco piezas dentro de la run\nwith mlflow.start_run(run_name=\"Mision_Tatooine\"):\n    # ⚙️ 1. Registra parametros\n    # 📡 2. Registra metricas\n    # 🔷 3. Registra los dos artefactos\n    # 🤖 4. Registra modelo\n    pass""",
    },
    {
        "id": "coruscant",
        "title": "Coruscant",
        "mode": "Misión saboteada",
        "n_estimators": 100,
        "max_depth": 10,
        "accent": "#43c8d8",
        "brief": "Corrige el intercambio entre parámetros, métricas y artefactos.",
        "theory": "Los parámetros describen decisiones anteriores al entrenamiento; las métricas son resultados numéricos posteriores; los artefactos son archivos. Coruscant contiene llamadas válidas colocadas en la categoría equivocada.",
        "context": """parametros = {\"dataset\": \"digits\", \"n_estimators\": 100, \"max_depth\": 10, \"test_size\": 0.2, \"random_state\": 42}\nmetricas = {\"accuracy\": accuracy, \"precision_weighted\": precision_weighted, \"recall_weighted\": recall_weighted, \"f1_weighted\": f1_weighted}\n# Repara el sabotaje y conserva dos artefactos y el modelo.""",
        "starter": """# ⚔️ MISIÓN SABOTEADA: corrige las categorías y completa las evidencias\nwith mlflow.start_run(run_name=\"Mision_Coruscant\"):\n    mlflow.log_metrics(parametros)  # BUG: decisiones previas\n    mlflow.log_params(metricas)    # BUG: resultados\n    mlflow.log_artifact(\"matriz_confusion.png\")\n    # 🔷 Falta el segundo artefacto\n    # 🤖 Falta conservar el modelo""",
    },
    {
        "id": "mustafar",
        "title": "Mustafar",
        "mode": "Misión autónoma",
        "n_estimators": 300,
        "max_depth": None,
        "accent": "#df6548",
        "brief": "Escribe el tracking 5–4–2–1 con la mínima ayuda del Archivo.",
        "theory": "En una run completa registrarás cinco parámetros, cuatro métricas, dos artefactos y un modelo. MLflow no entrena: documenta lo que scikit-learn ya ha producido para poder comparar y reutilizar.",
        "context": """# Dispones de: parametros, metricas, modelo, matriz_confusion.png y classification_report.json.\n# La run debe llamarse Mision_Mustafar y contener todas las llamadas.""",
        "starter": """# 🌋 MISIÓN AUTÓNOMA · CÓDIGO JEDI 5–4–2–1\n# ✦ Abre la run Mision_Mustafar y escribe aquí el tracking completo.\npass""",
    },
]


ORIENTATIVE_RESULTS = {
    "tatooine": {
        "accuracy": 0.9556,
        "precision_weighted": 0.9562,
        "recall_weighted": 0.9556,
        "f1_weighted": 0.9554,
        "recall_1": 0.9167,
        "recall_8": 0.8571,
    },
    "coruscant": {
        "accuracy": 0.9611,
        "precision_weighted": 0.9620,
        "recall_weighted": 0.9611,
        "f1_weighted": 0.9609,
        "recall_1": 0.9722,
        "recall_8": 0.8571,
    },
    "mustafar": {
        "accuracy": 0.9694,
        "precision_weighted": 0.9701,
        "recall_weighted": 0.9694,
        "f1_weighted": 0.9692,
        "recall_1": 1.0,
        "recall_8": 0.8571,
    },
}


MISSION_TEMPLATE = '''with mlflow.start_run(run_name="Mision_{name}"):
    mlflow.log_params(parametros)
    mlflow.log_metrics(metricas)
    mlflow.log_artifact("matriz_confusion.png")
    mlflow.log_artifact("classification_report.json")
    mlflow.sklearn.log_model(
        sk_model=modelo,
        artifact_path="modelo_digits",
    )'''


def chamber_by_index(index: int) -> dict | None:
    return CHAMBERS[index] if 0 <= index < len(CHAMBERS) else None


def mission_by_id(mission_id: str) -> dict:
    return next(item for item in MISSIONS if item["id"] == mission_id)
