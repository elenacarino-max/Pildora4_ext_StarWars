from __future__ import annotations


HOLOCRONS = [
    {
        "id": "consejo-desconfiado",
        "title": "Consejo desconfiado",
        "icon": "◈",
        "brief": "Una cifra no basta: revisad métricas, artefactos y una limitación.",
        "focus": "evidencias",
    },
    {
        "id": "recursos-limitados",
        "title": "Recursos limitados",
        "icon": "◒",
        "brief": "Valorad si la mejora de Mustafar compensa su mayor complejidad.",
        "focus": "complejidad",
    },
    {
        "id": "auditoria-imperial",
        "title": "Auditoría imperial",
        "icon": "⌁",
        "brief": "Otra persona debe poder reconstruir el experimento completo.",
        "focus": "trazabilidad",
    },
    {
        "id": "senado-galactico",
        "title": "Senado galáctico",
        "icon": "◎",
        "brief": "Explicad la decisión a un público no técnico con claridad.",
        "focus": "comunicación",
    },
    {
        "id": "lado-oscuro-metrica",
        "title": "El lado oscuro de la métrica",
        "icon": "◐",
        "brief": "Investigad qué comportamiento del dígito 8 oculta la cifra global.",
        "focus": "recall_8",
    },
    {
        "id": "rescate-prioritario",
        "title": "Rescate prioritario",
        "icon": "✦",
        "brief": "El recall del dígito 1 es crítico: reducid sus falsos negativos.",
        "focus": "recall_1",
    },
    {
        "id": "mision-produccion",
        "title": "Misión en producción",
        "icon": "⬡",
        "brief": "Combinad rendimiento, coste, trazabilidad y controles previos.",
        "focus": "producción",
    },
]


def holocron_by_id(holocron_id: str | None) -> dict | None:
    return next((item for item in HOLOCRONS if item["id"] == holocron_id), None)
