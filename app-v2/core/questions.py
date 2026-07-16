from __future__ import annotations

import secrets


TEAM_NAMES = [
    "Guardianes de Naboo",
    "Centinelas de Coruscant",
    "Exploradores de Tatooine",
    "Cronistas de Alderaan",
    "Custodios de Dagobah",
    "Vigías de Endor",
    "Navegantes de Hoth",
    "Forjadores de Mustafar",
    "Archiveros de Jedha",
    "Protectores de Lothal",
]


def _code(
    question_id: str,
    topic: str,
    title: str,
    theory: str,
    prompt: str,
    context: str,
    starter: str,
    solution: str,
    hints: list[str],
    **checks,
) -> dict:
    return {
        "id": question_id,
        "kind": "code",
        "topic": topic,
        "title": title,
        "theory": theory,
        "prompt": prompt,
        "context": context,
        "starter": starter,
        "solution": solution,
        "hints": hints,
        "checks": checks,
    }


def _choice(
    question_id: str,
    topic: str,
    title: str,
    theory: str,
    prompt: str,
    options: list[str],
    correct: str,
    hints: list[str],
) -> dict:
    return {
        "id": question_id,
        "kind": "choice",
        "topic": topic,
        "title": title,
        "theory": theory,
        "prompt": prompt,
        "context": "",
        "starter": "",
        "solution": correct,
        "options": options,
        "hints": hints,
        "checks": {},
    }


QUESTIONS = [
    # EXPERIMENT · 8
    _code("exp-01", "Experiment", "Abrir el archivo correcto", "Un Experiment agrupa runs que responden a una misma pregunta de trabajo.", "Completa la instrucción para seleccionar el experimento Biblioteca_Jedi_Digits.", "# 🌌 Todas las misiones de Digits deben quedar en el mismo archivo.", "# ✦ COMPLETA EL SELLO\npass", 'mlflow.set_experiment("Biblioteca_Jedi_Digits")', ["Busca una función que seleccione un experimento.", "Empieza por mlflow.set_...", "El nombre exacto es Biblioteca_Jedi_Digits."], expected_calls=["mlflow.set_experiment"], constant="Biblioteca_Jedi_Digits"),
    _code("exp-02", "Experiment", "Reparar el nombre del archivo", "El nombre estable de un Experiment permite encontrar juntas las runs de una actividad.", "Corrige el nombre para no crear un experimento distinto por error.", "# 🛰️ El Consejo acordó usar Biblioteca_Jedi_Digits.", 'mlflow.set_experiment("Biblioteca_Jedy_Digit")', 'mlflow.set_experiment("Biblioteca_Jedi_Digits")', ["Hay un error ortográfico.", "Comprueba Jedi.", "Comprueba también el plural Digits."], expected_calls=["mlflow.set_experiment"], constant="Biblioteca_Jedi_Digits"),
    _choice("exp-03", "Experiment", "¿Qué guarda la estantería?", "Experiment es el contenedor lógico; una Run es una ejecución concreta.", "¿Qué elemento debe agrupar Tatooine, Coruscant y Mustafar?", ["Un Experiment", "Tres métricas", "Un único artefacto", "El modelo sin sus runs"], "Un Experiment", ["Piensa en una carpeta de campañas.", "No es una ejecución individual.", "Agrupa runs relacionadas."]),
    _code("exp-04", "Experiment", "Separar campañas", "Conviene separar experimentos que responden a objetivos o datasets diferentes.", "Selecciona el experimento Biblioteca_Jedi_Digits antes de iniciar una run.", "# 🔭 Hoy trabajamos con imágenes de dígitos, no con el proyecto de churn.", "# Escribe una sola instrucción MLflow\npass", 'mlflow.set_experiment("Biblioteca_Jedi_Digits")', ["No necesitas abrir aún una run.", "Usa set_experiment.", "Respeta el nombre exacto."], expected_calls=["mlflow.set_experiment"], constant="Biblioteca_Jedi_Digits"),
    _choice("exp-05", "Experiment", "Detectar la mezcla peligrosa", "Mezclar objetivos distintos en un Experiment dificulta comparar runs con sentido.", "¿Qué práctica es más clara?", ["Un Experiment para Digits y otro para churn", "Una run para todos los datasets", "Guardar solo la última métrica", "Cambiar el nombre en cada ejecución"], "Un Experiment para Digits y otro para churn", ["La comparación necesita contexto común.", "Digits y churn responden a problemas distintos.", "Separa campañas por objetivo."]),
    _code("exp-06", "Experiment", "Bug de función", "set_experiment selecciona o crea el contenedor lógico de runs.", "Repara la función saboteada.", "# ⚔️ La llamada actual intenta abrir una run, pero necesitamos elegir el archivo.", 'mlflow.start_run("Biblioteca_Jedi_Digits")', 'mlflow.set_experiment("Biblioteca_Jedi_Digits")', ["start_run no selecciona el experimento.", "La función comienza por set_.", "Usa set_experiment."], expected_calls=["mlflow.set_experiment"], forbidden_calls=["mlflow.start_run"], constant="Biblioteca_Jedi_Digits"),
    _choice("exp-07", "Experiment", "Jerarquía del Archivo", "La jerarquía habitual es Experiment → Runs → parámetros, métricas y artefactos.", "¿Cuál es el orden correcto?", ["Experiment → Run → evidencias", "Run → Experiment → dataset", "Métrica → Run → Experiment", "Modelo → Experiment → Run"], "Experiment → Run → evidencias", ["Empieza por el contenedor más amplio.", "Después viene una ejecución.", "Las evidencias pertenecen a una run."]),
    _code("exp-08", "Experiment", "Nombre reproducible", "Usar un nombre constante evita dispersar ejecuciones entre contenedores casi iguales.", "Sustituye el nombre variable por el nombre común acordado.", "# 🔷 No uses el nombre del equipo en el Experiment; se guardará como etiqueta.", 'mlflow.set_experiment("Guardianes_Naboo")', 'mlflow.set_experiment("Biblioteca_Jedi_Digits")', ["El equipo no define la campaña.", "Todas las runs van a Biblioteca_Jedi_Digits.", "Cambia solo el argumento de texto."], expected_calls=["mlflow.set_experiment"], constant="Biblioteca_Jedi_Digits"),

    # RUN · 8
    _code("run-01", "Run", "Delimitar una misión", "Una Run representa una ejecución concreta con su configuración y resultados.", "Abre Mision_Tatooine usando un bloque with.", "# 🛰️ Todo lo registrado dentro pertenecerá a esta ejecución.", "# ✦ ABRE LA MISIÓN Y DEJA pass DENTRO\npass", 'with mlflow.start_run(run_name="Mision_Tatooine"):\n    pass', ["Usa start_run.", "Añade run_name.", "La llamada debe estar dentro de with."], expected_calls=["mlflow.start_run"], require_with=True, keyword="run_name"),
    _code("run-02", "Run", "Cerrar la compuerta automáticamente", "El bloque with cierra la Run incluso si ocurre un error dentro.", "Corrige el código para gestionar la run con with.", "# ⚔️ La llamada existe, pero no está delimitada como bloque.", 'mlflow.start_run(run_name="Mision_Coruscant")', 'with mlflow.start_run(run_name="Mision_Coruscant"):\n    pass', ["Falta un gestor de contexto.", "La línea empieza por with.", "Añade dos puntos y un cuerpo indentado."], expected_calls=["mlflow.start_run"], require_with=True, keyword="run_name"),
    _choice("run-03", "Run", "Una ejecución, una historia", "Cada Run conserva la combinación exacta de parámetros, métricas y artefactos de un entrenamiento.", "¿Qué diferencia principalmente dos runs?", ["Su ejecución y evidencias registradas", "El color de la interfaz", "La carpeta del navegador", "El nombre del equipo únicamente"], "Su ejecución y evidencias registradas", ["Piensa en qué se compara en MLflow.", "Una run conserva configuración y resultados.", "No depende del navegador."]),
    _code("run-04", "Run", "Nombrar Mustafar", "Un run_name descriptivo facilita reconocer una ejecución en la interfaz.", "Abre una run llamada Mision_Mustafar.", "# 🌋 Esta será la tercera configuración de Random Forest.", "with mlflow.start_run():\n    pass", 'with mlflow.start_run(run_name="Mision_Mustafar"):\n    pass', ["La estructura with ya es correcta.", "Falta el argumento run_name.", "El valor exacto es Mision_Mustafar."], expected_calls=["mlflow.start_run"], require_with=True, keyword="run_name", constant="Mision_Mustafar"),
    _choice("run-05", "Run", "Evitar mezclar resultados", "Si dos entrenamientos se registran en la misma Run, se pierde la separación entre configuraciones.", "¿Cuántas runs necesitan tres entrenamientos comparables?", ["Tres", "Una", "Seis", "Ninguna"], "Tres", ["Cada entrenamiento es una ejecución.", "No mezcles configuraciones.", "Una run por entrenamiento."]),
    _code("run-06", "Run", "Bug de indentación conceptual", "Los registros de una ejecución deben quedar dentro del bloque de su Run.", "Añade una métrica dentro de la run manteniendo una indentación válida.", "# 📡 accuracy ya ha sido calculada.", 'with mlflow.start_run(run_name="Mision_Tatooine"):\n    pass', 'with mlflow.start_run(run_name="Mision_Tatooine"):\n    mlflow.log_metric("accuracy", accuracy)', ["Sustituye pass.", "Usa log_metric.", "La línea debe tener cuatro espacios."], expected_calls=["mlflow.start_run", "mlflow.log_metric"], require_with=True),
    _choice("run-07", "Run", "ID frente a nombre", "El run_id es un identificador único; run_name es una etiqueta legible.", "¿Qué dato es seguro que no se repite?", ["run_id", "run_name", "accuracy", "n_estimators"], "run_id", ["Los nombres pueden reutilizarse.", "Las métricas pueden coincidir.", "MLflow genera un identificador único."]),
    _code("run-08", "Run", "Reparar la llamada", "start_run abre el contexto de una ejecución; set_experiment selecciona el grupo.", "Reemplaza la llamada incorrecta y abre Mision_Coruscant.", "# ⚔️ El experimento ya fue seleccionado antes.", 'with mlflow.set_experiment("Mision_Coruscant"):\n    pass', 'with mlflow.start_run(run_name="Mision_Coruscant"):\n    pass', ["No selecciones otro experimento.", "Necesitas start_run.", "Usa run_name dentro de with."], expected_calls=["mlflow.start_run"], forbidden_calls=["mlflow.set_experiment"], require_with=True),

    # PARAMETERS · 9
    _code("par-01", "Parameters", "Registrar la estrategia", "Los Parameters son decisiones conocidas antes de entrenar.", "Registra todo el diccionario parametros de una vez.", "parametros = {\n    \"n_estimators\": 100,\n    \"max_depth\": 10,\n    \"random_state\": 42,\n}", "# ⚙️ REGISTRA LA ESTRATEGIA\npass", "mlflow.log_params(parametros)", ["No registres una métrica.", "La función termina en params.", "Pasa el diccionario parametros."], expected_calls=["mlflow.log_params"]),
    _code("par-02", "Parameters", "Parámetro individual", "log_param registra una pareja nombre-valor; log_params registra un diccionario.", "Registra n_estimators con valor 50.", "# 🛠️ Esta decisión se toma antes de model.fit().", "pass", 'mlflow.log_param("n_estimators", 50)', ["Usa la versión singular.", "El primer argumento es el nombre.", "El segundo argumento es 50."], expected_calls=["mlflow.log_param"], constant="n_estimators"),
    _choice("par-03", "Parameters", "Antes o después", "Un parámetro configura el entrenamiento antes de que el modelo produzca predicciones.", "¿Cuál es un parámetro?", ["max_depth", "accuracy", "recall_8", "matriz_confusion.png"], "max_depth", ["Busca una decisión previa.", "No elijas un resultado.", "Controla la profundidad del bosque."]),
    _code("par-04", "Parameters", "Bug: accuracy no es estrategia", "accuracy se calcula después de predecir, por lo que es una métrica.", "Corrige la categoría usada para registrar accuracy.", "accuracy = 0.96", 'mlflow.log_param("accuracy", accuracy)', 'mlflow.log_metric("accuracy", accuracy)', ["El valor es un resultado.", "Usa log_metric.", "Cambia param por metric."], expected_calls=["mlflow.log_metric"], forbidden_calls=["mlflow.log_param"]),
    _choice("par-05", "Parameters", "Configuración reproducible", "Guardar random_state ayuda a repetir la misma partición o entrenamiento.", "¿Por qué registrar random_state?", ["Para facilitar la reproducibilidad", "Para aumentar siempre accuracy", "Para crear un PNG", "Para sustituir el dataset"], "Para facilitar la reproducibilidad", ["No garantiza mejor calidad.", "Controla el azar.", "Permite repetir condiciones."]),
    _code("par-06", "Parameters", "Diccionario completo", "Registrar parámetros juntos reduce omisiones y mantiene una estructura legible.", "Repara la función: parametros es un diccionario.", "parametros = {\"test_size\": 0.2, \"random_state\": 42}", "mlflow.log_param(parametros)", "mlflow.log_params(parametros)", ["La entrada contiene varias parejas.", "Necesitas la forma plural.", "Usa log_params."], expected_calls=["mlflow.log_params"], forbidden_calls=["mlflow.log_param"]),
    _choice("par-07", "Parameters", "Comparación justa", "Para explicar un cambio de métricas hay que conocer qué parámetros variaron entre runs.", "¿Qué comparación es interpretable?", ["Runs con parámetros y métricas registrados", "Solo dos capturas de pantalla", "Solo los nombres de equipo", "Una métrica sin configuración"], "Runs con parámetros y métricas registrados", ["Necesitas causas y resultados.", "La configuración explica diferencias.", "Registra ambos tipos de datos."]),
    _code("par-08", "Parameters", "Profundidad sin límite", "None puede ser una decisión de configuración válida para max_depth.", "Registra max_depth con el valor None.", "# 🌲 Mustafar deja crecer los árboles sin límite explícito.", "pass", 'mlflow.log_param("max_depth", None)', ["Usa log_param singular.", "El nombre es max_depth.", "None no lleva comillas."], expected_calls=["mlflow.log_param"], constant="max_depth"),
    _choice("par-09", "Parameters", "Cinco datos de estrategia", "Dataset, n_estimators, max_depth, test_size y random_state describen la configuración usada.", "¿Cuál no pertenece al grupo de cinco parámetros?", ["f1_weighted", "dataset", "test_size", "n_estimators"], "f1_weighted", ["Busca un valor calculado al evaluar.", "F1 resume rendimiento.", "Los demás se conocen antes de entrenar."]),

    # METRICS · 9
    _code("met-01", "Metrics", "Registrar el informe", "Las Metrics son resultados numéricos calculados después de evaluar.", "Registra el diccionario metricas completo.", "metricas = {\n    \"accuracy\": accuracy,\n    \"f1_weighted\": f1_weighted,\n}", "# 📡 ENVÍA EL INFORME AL CONSEJO\npass", "mlflow.log_metrics(metricas)", ["No son parámetros.", "Usa la forma plural.", "La función es log_metrics."], expected_calls=["mlflow.log_metrics"]),
    _code("met-02", "Metrics", "Una métrica individual", "log_metric registra un resultado numérico con su nombre.", "Registra accuracy.", "accuracy = 0.9611", "pass", 'mlflow.log_metric("accuracy", accuracy)', ["Usa singular.", "El nombre debe ser accuracy.", "El valor es la variable accuracy."], expected_calls=["mlflow.log_metric"], constant="accuracy"),
    _choice("met-03", "Metrics", "Accuracy no lo cuenta todo", "Accuracy resume aciertos globales, pero puede ocultar clases con peor comportamiento.", "¿Qué dato ayuda a revisar específicamente el dígito 8?", ["recall_8", "n_estimators", "run_name", "artifact_path"], "recall_8", ["Busca una métrica por clase.", "Interesa cuántos ochos se recuperan.", "Usa recall de la clase 8."]),
    _code("met-04", "Metrics", "Bug: árboles como resultado", "n_estimators configura el bosque y no es un resultado de evaluación.", "Corrige cómo se registra n_estimators.", "n_estimators = 100", 'mlflow.log_metric("n_estimators", n_estimators)', 'mlflow.log_param("n_estimators", n_estimators)', ["Se conoce antes del entrenamiento.", "Es un parámetro.", "Cambia metric por param."], expected_calls=["mlflow.log_param"], forbidden_calls=["mlflow.log_metric"]),
    _choice("met-05", "Metrics", "F1 ponderada", "F1 weighted combina precisión y recall ponderando cada clase por su frecuencia.", "¿Cuándo aporta información F1 weighted?", ["Al resumir equilibrio entre precisión y recall", "Al elegir el número de árboles antes de entrenar", "Al guardar una imagen", "Al crear el Experiment"], "Al resumir equilibrio entre precisión y recall", ["Es una métrica de evaluación.", "Combina dos perspectivas.", "No configura el modelo."]),
    _code("met-06", "Metrics", "Cuatro señales", "Registrar varias métricas evita decidir con una sola cifra.", "Registra accuracy, precision_weighted, recall_weighted y f1_weighted mediante un diccionario.", "metricas = {\n    \"accuracy\": accuracy,\n    \"precision_weighted\": precision_weighted,\n    \"recall_weighted\": recall_weighted,\n    \"f1_weighted\": f1_weighted,\n}", "pass", "mlflow.log_metrics(metricas)", ["El diccionario ya contiene cuatro señales.", "No necesitas cuatro llamadas.", "Usa log_metrics(metricas)."], expected_calls=["mlflow.log_metrics"]),
    _choice("met-07", "Metrics", "Resultado frente a evidencia", "Una métrica permite ordenar runs; un artefacto ayuda a explicar por qué fallan.", "¿Qué combinación ofrece mejor diagnóstico?", ["F1 y matriz de confusión", "run_name y color", "Solo accuracy", "Solo n_estimators"], "F1 y matriz de confusión", ["Combina resumen y detalle.", "Una cifra y una evidencia visual.", "La matriz muestra confusiones entre clases."]),
    _code("met-08", "Metrics", "Nombre coherente", "Usar nombres de métricas constantes permite compararlas automáticamente entre runs.", "Corrige el nombre para usar f1_weighted.", "f1_weighted = 0.96", 'mlflow.log_metric("f1", f1_weighted)', 'mlflow.log_metric("f1_weighted", f1_weighted)', ["La llamada es correcta.", "El problema está en la etiqueta.", "Usa exactamente f1_weighted."], expected_calls=["mlflow.log_metric"], constant="f1_weighted"),
    _choice("met-09", "Metrics", "Momento de registro", "Las métricas se obtienen después de generar predicciones sobre datos de evaluación.", "¿En qué momento se conoce recall?", ["Después de comparar predicciones y valores reales", "Antes de cargar los datos", "Al elegir random_state", "Al crear el nombre de la run"], "Después de comparar predicciones y valores reales", ["Recall depende de aciertos y fallos.", "Necesita predicciones.", "Se calcula durante la evaluación."]),

    # ARTIFACTS · 8
    _code("art-01", "Artifacts", "Guardar la matriz", "Un Artifact es un archivo asociado a una Run: imagen, JSON, tabla o informe.", "Registra matriz_confusion.png.", "# 🔷 La imagen ya existe en el directorio de la misión.", "pass", 'mlflow.log_artifact("matriz_confusion.png")', ["No uses log_metric.", "La función termina en artifact.", "Pasa la ruta del PNG."], expected_calls=["mlflow.log_artifact"], constant="matriz_confusion.png"),
    _choice("art-02", "Artifacts", "Clasificar la evidencia", "Los artefactos conservan información más rica que una cifra aislada.", "¿Cuál debe registrarse como Artifact?", ["classification_report.json", "accuracy = 0.96", "max_depth = 10", "random_state = 42"], "classification_report.json", ["Busca un archivo.", "JSON conserva un informe estructurado.", "Los demás son valores escalares."]),
    _code("art-03", "Artifacts", "Dos evidencias", "La matriz visual y el informe JSON permiten inspeccionar errores por clase.", "Registra los dos archivos.", "# 📜 Ambos archivos se generaron tras evaluar el modelo.", "# Añade dos llamadas\npass", 'mlflow.log_artifact("matriz_confusion.png")\nmlflow.log_artifact("classification_report.json")', ["Necesitas dos llamadas iguales.", "Cambia únicamente la ruta.", "Usa log_artifact para PNG y JSON."], expected_calls=["mlflow.log_artifact"], min_call_count=2),
    _code("art-04", "Artifacts", "Bug: imagen como métrica", "Una ruta de imagen no es un número y no puede interpretarse como métrica.", "Corrige la llamada saboteada.", "archivo = \"matriz_confusion.png\"", 'mlflow.log_metric("matriz", archivo)', "mlflow.log_artifact(archivo)", ["No es un valor numérico.", "Es un archivo.", "Usa log_artifact."], expected_calls=["mlflow.log_artifact"], forbidden_calls=["mlflow.log_metric"]),
    _choice("art-05", "Artifacts", "Explicar el error", "La matriz de confusión indica qué clases se confunden entre sí.", "¿Qué evidencia consultarías si el recall del 8 es bajo?", ["matriz_confusion.png", "run_name", "random_state solamente", "nombre del equipo"], "matriz_confusion.png", ["Necesitas ver a qué clase van los ochos.", "Busca una tabla visual de errores.", "La matriz de confusión muestra esos cruces."]),
    _code("art-06", "Artifacts", "Ruta legible", "artifact_path organiza archivos dentro del repositorio de una Run.", "Guarda la matriz dentro de la carpeta evidencias.", "# 🗂️ La interfaz mostrará evidencias/matriz_confusion.png.", "pass", 'mlflow.log_artifact("matriz_confusion.png", artifact_path="evidencias")', ["La función sigue siendo log_artifact.", "Añade el argumento artifact_path.", "El valor de la carpeta es evidencias."], expected_calls=["mlflow.log_artifact"], keyword="artifact_path"),
    _choice("art-07", "Artifacts", "Persistencia del informe", "Si el informe solo queda en memoria o en la terminal, se pierde el contexto de la Run.", "¿Por qué registrar el JSON?", ["Para conservar el detalle junto a la Run", "Para aumentar automáticamente F1", "Para cambiar los parámetros", "Para cerrar el Experiment"], "Para conservar el detalle junto a la Run", ["Registrar no mejora el modelo.", "Sirve para consultar después.", "La evidencia queda vinculada a la ejecución."]),
    _code("art-08", "Artifacts", "Nombre exacto del informe", "Las rutas deben coincidir con archivos realmente generados.", "Corrige la extensión del informe.", "# El proceso genera classification_report.json.", 'mlflow.log_artifact("classification_report.png")', 'mlflow.log_artifact("classification_report.json")', ["La función es correcta.", "El informe no es una imagen.", "La extensión correcta es .json."], expected_calls=["mlflow.log_artifact"], constant="classification_report.json"),

    # MODEL · 8
    _code("mod-01", "Model", "Conservar el Jedi entrenado", "Registrar el Model permite cargarlo después sin volver a entrenar.", "Guarda modelo con la integración de scikit-learn.", "# 🤖 modelo es un RandomForestClassifier ya entrenado.", "# ✦ COMPLETA EL ARCHIVO DEL MODELO\npass", 'mlflow.sklearn.log_model(sk_model=modelo, artifact_path="modelo_digits")', ["Usa la integración mlflow.sklearn.", "La función es log_model.", "Incluye sk_model y artifact_path."], expected_calls=["mlflow.sklearn.log_model"], keywords=["sk_model", "artifact_path"]),
    _choice("mod-02", "Model", "Métricas no son modelo", "Las métricas describen rendimiento, pero no contienen el objeto capaz de predecir.", "¿Qué permite reutilizar directamente el clasificador?", ["El modelo registrado", "Solo accuracy", "Solo la matriz", "El nombre del Experiment"], "El modelo registrado", ["Busca el objeto que predice.", "Una cifra no ejecuta inferencias.", "Debes conservar el clasificador entrenado."]),
    _code("mod-03", "Model", "Bug de argumento", "log_model necesita saber qué objeto guardar y dónde colocarlo.", "Corrige el nombre del argumento model.", "# ⚔️ El objeto correcto se llama modelo.", 'mlflow.sklearn.log_model(model=modelo, artifact_path="modelo_digits")', 'mlflow.sklearn.log_model(sk_model=modelo, artifact_path="modelo_digits")', ["artifact_path ya está bien.", "La integración espera sk_model.", "Cambia model por sk_model."], expected_calls=["mlflow.sklearn.log_model"], keywords=["sk_model", "artifact_path"]),
    _code("mod-04", "Model", "Destino del modelo", "artifact_path asigna un nombre legible a la carpeta del modelo dentro de la Run.", "Guarda el modelo bajo modelo_digits.", "# 🗃️ Evita nombres genéricos como model1.", 'mlflow.sklearn.log_model(sk_model=modelo, artifact_path="model1")', 'mlflow.sklearn.log_model(sk_model=modelo, artifact_path="modelo_digits")', ["sk_model ya es correcto.", "Revisa la ruta de destino.", "Usa exactamente modelo_digits."], expected_calls=["mlflow.sklearn.log_model"], keywords=["sk_model", "artifact_path"], constant="modelo_digits"),
    _choice("mod-05", "Model", "Firma del modelo", "Una signature documenta la forma de las entradas y salidas esperadas.", "¿Qué riesgo reduce una firma?", ["Enviar datos con estructura incompatible", "Elegir pocos árboles", "Confundir una métrica con un parámetro", "Repetir un run_name"], "Enviar datos con estructura incompatible", ["Piensa en el contrato de entrada.", "Describe columnas o formas.", "Ayuda a validar inferencias."]),
    _code("mod-06", "Model", "Modelo dentro de la Run", "El modelo debe registrarse mientras la Run correspondiente está abierta.", "Completa el bloque para guardar modelo.", "with mlflow.start_run(run_name=\"Mision_Mustafar\"):\n    # El entrenamiento ya ha terminado.", "with mlflow.start_run(run_name=\"Mision_Mustafar\"):\n    pass", 'with mlflow.start_run(run_name="Mision_Mustafar"):\n    mlflow.sklearn.log_model(sk_model=modelo, artifact_path="modelo_digits")', ["Sustituye pass dentro del bloque.", "Usa mlflow.sklearn.log_model.", "Mantén cuatro espacios de indentación."], expected_calls=["mlflow.start_run", "mlflow.sklearn.log_model"], require_with=True, keywords=["sk_model", "artifact_path"]),
    _choice("mod-07", "Model", "Reproducir frente a reutilizar", "Parámetros y código ayudan a reproducir; el modelo registrado permite reutilizar exactamente el objeto obtenido.", "¿Qué opción evita reentrenar para predecir?", ["Cargar el modelo registrado", "Leer solo f1_weighted", "Cambiar run_name", "Crear otro Experiment"], "Cargar el modelo registrado", ["Quieres usar el objeto existente.", "No necesitas repetir fit.", "MLflow puede cargar el modelo guardado."]),
    _code("mod-08", "Model", "Integración correcta", "Cada framework dispone de integraciones específicas para serializar modelos.", "Corrige la integración para un RandomForestClassifier de scikit-learn.", "# 🌲 modelo procede de sklearn.ensemble.", 'mlflow.pytorch.log_model(sk_model=modelo, artifact_path="modelo_digits")', 'mlflow.sklearn.log_model(sk_model=modelo, artifact_path="modelo_digits")', ["No es un modelo de PyTorch.", "La librería es scikit-learn.", "Usa mlflow.sklearn.log_model."], expected_calls=["mlflow.sklearn.log_model"], keywords=["sk_model", "artifact_path"]),
]


QUESTION_BY_ID = {item["id"]: item for item in QUESTIONS}
TOPICS = ["Experiment", "Run", "Parameters", "Metrics", "Artifacts", "Model"]


def choose_session_question_ids() -> list[str]:
    """Elige un reto por concepto para mantener cobertura y variar cada sesión."""
    return [secrets.choice([q for q in QUESTIONS if q["topic"] == topic])["id"] for topic in TOPICS]


def questions_from_ids(question_ids: list[str]) -> list[dict]:
    return [QUESTION_BY_ID[item] for item in question_ids if item in QUESTION_BY_ID]
