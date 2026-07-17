# MLflow Jedi · La Cámara de los Experimentos Perdidos

Aplicación didáctica de Streamlit para practicar el ciclo completo de tracking
de experimentos: parámetros, métricas, artefactos y modelos registrados con
MLflow sobre el dataset Digits.

## Aplicación publicada

**[Abrir MLflow Jedi en Streamlit](https://pildora4extstarwars-14.streamlit.app/)**

El despliegue público permite probar y compartir la actividad sin instalar el
proyecto. El profesorado debe crear primero una sesión y compartir el código
`JEDI-XXXX` con los equipos. La ejecución local y Docker, descritas más abajo,
continúan disponibles para pruebas y para instalaciones con almacenamiento
persistente propio.

## Funcionalidad

### Experiencia del alumnado

- acceso mediante un código de sesión `JEDI-XXXX` y diez nombres de equipo;
- seis cámaras, seleccionadas de un banco de 50 preguntas (una por concepto);
- hasta cinco intentos y tres pistas progresivas por cámara;
- editor de Python y validación estática mediante AST;
- tres misiones de Random Forest: Tatooine, Coruscant y Mustafar;
- tracking real con cinco parámetros, cuatro métricas globales, dos recalls por
  clase, dos artefactos y un modelo;
- comparación de runs, matriz de confusión e informe por dígito;
- siete holocrones posibles y una defensa final basada en evidencias.

### Panel del profesorado

- creación y cierre de sesiones;
- seguimiento de equipos, puntuaciones, intentos y pistas;
- aviso global, desbloqueo de progreso, reinicio y reasignación de holocrón;
- consulta de defensas;
- exportación de un respaldo completo en JSON y de un resumen en CSV.

## Requisitos

Elige una de estas opciones:

- Docker con Docker Compose; o
- Python 3.12 para la ejecución local.

## Configuración

Copia el archivo de ejemplo y edita sus valores:

```powershell
Copy-Item .env.example .env
```

| Variable | Uso | Valor de ejemplo |
|---|---|---|
| `MLFLOW_JEDI_TEACHER_PASSWORD` | Contraseña del panel docente | `1234` |
| `MLFLOW_JEDI_DATA_DIR` | Directorio de bases de datos y artefactos | `./data` |
| `MLFLOW_JEDI_MAX_TEAMS` | Máximo de equipos por sesión | `10` |

Cambia siempre la contraseña de ejemplo antes de compartir la aplicación. El
archivo `.env` está excluido de Git.

## Ejecución local

Desde este directorio (`app-v2/`):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Abre <http://localhost:8501> y sigue este flujo:

1. entra en **Profesorado** y crea una sesión;
2. comparte el código generado con los equipos;
3. cada equipo entra en **Alumnado** y elige un nombre disponible.

## Ejecución con Docker

```powershell
docker compose up --build
```

La aplicación queda disponible en <http://localhost:8501>. Para detenerla:

```powershell
docker compose down
```

El volumen `mlflow_jedi_data` conserva sesiones, intentos, puntuaciones, runs,
modelos y artefactos entre reinicios y reconstrucciones. El comando
`docker compose down -v` elimina ese volumen y, por tanto, sus datos.

## Pruebas

Con las dependencias instaladas, ejecuta:

```powershell
python -m unittest discover -s tests -v
```

Las pruebas cubren el banco de preguntas, el contenido de las misiones, la
validación segura de código y las operaciones principales de la base de datos.

## Datos y persistencia

Por defecto, la carpeta `data/` contiene:

```text
data/
├── game.db       # sesiones, equipos, intentos, puntuaciones y defensas
├── mlflow.db     # metadatos de tracking de MLflow
└── artifacts/    # matrices, informes y artefactos de MLflow
```

Para hacer una copia de seguridad, exporta JSON/CSV desde el panel docente y
conserva también `data/` con la aplicación detenida. Consulta la
[`Guía de mantenimiento`](docs/GUIA_MANTENIMIENTO.md) antes de actualizar o
trasladar una instalación.

## Seguridad y alcance

El texto escrito por el alumnado **no se ejecuta**. La aplicación analiza su
estructura con `ast`, rechaza imports y llamadas no autorizadas y, cuando la
solución es válida, entrena una plantilla interna controlada.

La contraseña docente es una protección básica pensada para una actividad de
aula. Si se publica fuera de una red de confianza, deben añadirse HTTPS,
autenticación y controles de acceso propios del entorno de despliegue.

## Documentación

- [`Guía rápida para el profesorado`](docs/GUIA_PROFESORADO.md)
- [`Mantenimiento, datos y copias de seguridad`](docs/GUIA_MANTENIMIENTO.md)
- [Material docente y notebooks del proyecto](../README.md)

## Contingencia

Si la aplicación o la conectividad fallan, utiliza los notebooks y documentos
de las carpetas [`notebooks/`](../notebooks/) y [`docs/`](../docs/) de la raíz
del repositorio.
