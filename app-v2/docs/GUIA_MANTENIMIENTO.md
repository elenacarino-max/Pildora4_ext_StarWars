# Mantenimiento, datos y copias de seguridad

## Datos persistentes

La carpeta `data/` contiene:

- `game.db`: sesiones, equipos, intentos, progreso, puntuación y defensas;
- `mlflow.db`: metadatos de tracking;
- `artifacts/`: matrices, informes y copias locales asociadas a las runs.

En Docker se monta como el volumen `mlflow_jedi_data`. No despliegues la app en un servicio que elimine ese volumen al suspender el proyecto.

## Copias

- Exporta JSON y CSV desde el panel docente al terminar cada sesión.
- Detén la aplicación antes de copiar los archivos SQLite manualmente.
- Conserva una copia de `data/` y del código de la misma versión.

## Variables

- `MLFLOW_JEDI_TEACHER_PASSWORD`: contraseña del panel docente.
- `MLFLOW_JEDI_DATA_DIR`: ruta persistente para bases y artefactos.
- `MLFLOW_JEDI_MAX_TEAMS`: máximo de equipos por sesión.

## Actualizaciones

1. Haz copia de `data/`.
2. Ejecuta las pruebas.
3. Construye una nueva imagen Docker.
4. Arranca usando el mismo volumen persistente.
5. Comprueba una sesión de prueba antes de usarla en clase.
