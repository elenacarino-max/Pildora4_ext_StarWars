# Guía rápida para el profesorado

## Antes de la sesión

1. Arranca la aplicación y entra en **Profesorado**.
2. Crea una sesión y comparte el código `JEDI-XXXX`.
3. Organiza equipos de tres: Navegante, Escriba y Auditor. Cada grupo elige uno de los diez nombres del desplegable.
4. Crea una sesión nueva: la aplicación elegirá seis preguntas al azar, una de cada concepto esencial de MLflow.

### Qué significa conservar `data/`

No necesitas revisar ninguna carpeta durante la clase. La aplicación guarda automáticamente sesiones, puntuaciones, intentos, runs, modelos y artefactos.

- **Con Docker:** `docker-compose.yml` ya conecta esos datos al volumen `mlflow_jedi_data`. El volumen vive fuera del contenedor, así que `docker compose down` o reconstruir la imagen no borra la actividad.
- **Sin Docker:** los datos quedan en `app-v2/data/`. No elimines esa carpeta mientras necesites conservar sesiones anteriores.
- `docker compose down -v` sí elimina expresamente el volumen. No uses `-v` salvo que quieras empezar desde cero.

## Durante la actividad

- Las seis cámaras se abren en orden y cada solución válida suma 20 puntos.
- Cada sesión recibe una selección distinta procedente de un banco de 50 preguntas.
- Cada pista resta 5 puntos y revela progresivamente concepto, categoría y sintaxis.
- Hay cinco intentos por cámara. Tras cinco fallos se muestra la solución, se restan 10 puntos adicionales y el equipo avanza para evitar bloqueos.
- Las misiones suman 30 puntos; completar las tres añade 15.
- Tras completar las tres misiones, el equipo compara las runs y pulsa **Ejecuten Orden 66** para revelar su tarjeta específica. La tarjeta incluye el encargo, cuatro pasos y el formato de la entrega, y puede descargarse.
- La matriz de confusión y `classification_report.json` se consultan directamente tanto en **Comparador** como en **Consejo**. Deben revisarlos antes de rellenar “Artefacto consultado”.
- La defensa completa suma 25 puntos.
- Desde el panel puedes desbloquear una cámara, reiniciar un equipo, enviar un aviso global o reasignar un holocrón.

## Mensaje técnico central

**Scikit-learn entrena. MLflow registra. El Consejo compara y decide.**

La app siempre muestra el término narrativo junto al profesional: Estrategia — Parameters, Informe — Metrics, Holocrón — Artifact.

## Contingencia

Si la aplicación falla, utiliza los notebooks y documentos conservados en la raíz del repositorio. No los elimines: forman parte del plan de continuidad.
