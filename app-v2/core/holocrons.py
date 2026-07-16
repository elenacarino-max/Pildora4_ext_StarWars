from __future__ import annotations


HOLOCRONS = [
    {
        "id": "consejo-desconfiado",
        "title": "Consejo desconfiado",
        "icon": "◈",
        "brief": "Una cifra no basta: revisad métricas, artefactos y una limitación.",
        "focus": "evidencias",
        "task": "Convenced a un Consejo que no acepta una recomendación basada únicamente en accuracy.",
        "steps": [
            "Comparad las tres runs usando al menos dos métricas.",
            "Abrid la matriz de confusión o el informe JSON de la run elegida.",
            "Señalad un error concreto y una limitación de vuestra decisión.",
            "Elegid una run y descartad otra con una razón basada en evidencias.",
        ],
        "deliverable": "Defensa de 45–60 segundos con dos métricas, un artefacto, una limitación y una recomendación.",
    },
    {
        "id": "recursos-limitados",
        "title": "Recursos limitados",
        "icon": "◒",
        "brief": "Valorad si la mejora de Mustafar compensa su mayor complejidad.",
        "focus": "complejidad",
        "task": "El Archivo dispone de recursos limitados: debéis decidir si merece la pena conservar el bosque más grande.",
        "steps": [
            "Comparad 50, 100 y 300 árboles junto con accuracy y F1 weighted.",
            "Calculad si la mejora de Mustafar frente a una run menor es relevante.",
            "Consultad un artefacto para comprobar que la mejora no oculta errores por clase.",
            "Recomendad la run con mejor equilibrio entre rendimiento y coste.",
        ],
        "deliverable": "Decisión argumentada que mencione la diferencia de rendimiento y el coste relativo en número de árboles.",
    },
    {
        "id": "auditoria-imperial",
        "title": "Auditoría imperial",
        "icon": "⌁",
        "brief": "Otra persona debe poder reconstruir el experimento completo.",
        "focus": "trazabilidad",
        "task": "Preparad una auditoría que permita a otro equipo entender y reconstruir la run seleccionada.",
        "steps": [
            "Identificad los cinco parámetros registrados en la run.",
            "Comprobad las cuatro métricas y los dos artefactos.",
            "Verificad que existe un modelo registrado y un run_id.",
            "Explicad qué información faltaría para una reproducción perfecta.",
        ],
        "deliverable": "Informe oral de trazabilidad: qué puede reproducirse, qué evidencia existe y qué limitación permanece.",
    },
    {
        "id": "senado-galactico",
        "title": "Senado galáctico",
        "icon": "◎",
        "brief": "Explicad la decisión a un público no técnico con claridad.",
        "focus": "comunicación",
        "task": "Presentad la elección al Senado sin depender de jerga técnica ni de una tabla llena de decimales.",
        "steps": [
            "Traducid la métrica principal a una frase comprensible.",
            "Usad la matriz de confusión para contar un ejemplo concreto de error.",
            "Explicad por qué descartáis una alternativa.",
            "Cerrad con una recomendación y una precaución.",
        ],
        "deliverable": "Explicación de 45–60 segundos comprensible para alguien que no conoce MLflow.",
    },
    {
        "id": "lado-oscuro-metrica",
        "title": "El lado oscuro de la métrica",
        "icon": "◐",
        "brief": "Investigad qué comportamiento del dígito 8 oculta la cifra global.",
        "focus": "recall_8",
        "task": "Descubrid si una accuracy elevada está ocultando fallos importantes al reconocer el dígito 8.",
        "steps": [
            "Comparad accuracy y recall_8 en las tres runs.",
            "Abrid la matriz de confusión y localizad la fila del dígito 8.",
            "Indicad con qué dígitos se confunde y en qué run ocurre menos.",
            "Elegid la run priorizando la evidencia relevante para el 8.",
        ],
        "deliverable": "Recomendación que contraste la métrica global con recall_8 y un hallazgo de la matriz.",
    },
    {
        "id": "rescate-prioritario",
        "title": "Rescate prioritario",
        "icon": "✦",
        "brief": "El recall del dígito 1 es crítico: reducid sus falsos negativos.",
        "focus": "recall_1",
        "task": "El rescate depende de detectar tantos unos reales como sea posible, aunque la accuracy global no sea la máxima.",
        "steps": [
            "Comparad recall_1 en las tres runs.",
            "Consultad la matriz o el JSON para verificar los errores del dígito 1.",
            "Comprobad qué se sacrifica al priorizar ese recall.",
            "Elegid una run y justificad el riesgo aceptado.",
        ],
        "deliverable": "Decisión centrada en falsos negativos del dígito 1, con evidencia y un posible efecto secundario.",
    },
    {
        "id": "mision-produccion",
        "title": "Misión en producción",
        "icon": "⬡",
        "brief": "Combinad rendimiento, coste, trazabilidad y controles previos.",
        "focus": "producción",
        "task": "Actuad como responsables de producción y decidid qué run está preparada para salir del laboratorio.",
        "steps": [
            "Comparad rendimiento global y comportamiento por clase.",
            "Revisad parámetros, artefactos y existencia del modelo registrado.",
            "Valorad complejidad, reproducibilidad y riesgo de error.",
            "Proponed un control adicional antes del despliegue.",
        ],
        "deliverable": "Recomendación de producción con evidencia, coste, riesgo y una condición previa al despliegue.",
    },
]


def holocron_by_id(holocron_id: str | None) -> dict | None:
    return next((item for item in HOLOCRONS if item["id"] == holocron_id), None)
