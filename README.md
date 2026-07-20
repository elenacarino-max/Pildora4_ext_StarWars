# Píldora extendida de MLflow · Biblioteca Jedi

Material docente para aprender **tracking de experimentos con MLflow** a partir
del dataset Digits de scikit-learn y una narrativa inspirada en Star Wars.

El repositorio combina una aplicación interactiva para el aula con documentos
y notebooks que sirven como apoyo, práctica y plan de contingencia.


## 📚 Documentación del proyecto

Consulta la documentación completa y los diagramas del proyecto en:

👉 [Documentación en DeepWiki](https://deepwiki.com/elenacarino-max/Pildora4_ext_StarWars)

## Aplicación interactiva

La versión principal está en [`app-v2/`](app-v2/). Es una aplicación Streamlit
en la que el alumnado:

1. supera seis cámaras sobre Experiment, Run, Parameters, Metrics, Artifacts y
   Model;
2. reconstruye tres experimentos reales de Random Forest;
3. compara métricas y artefactos registrados con MLflow;
4. defiende una recomendación basada en evidencias.

El profesorado dispone de un panel para crear sesiones, seguir el progreso,
enviar avisos, desbloquear cámaras, reasignar retos y exportar resultados.

### Aplicación publicada

La versión desplegada está disponible en:

**[Abrir MLflow Jedi en Streamlit](https://pildora4extstarwars-14.streamlit.app/)**

Para crear una sesion hay que entrar como profesor con esta contraseña Jedi!KEoErJmGO7Ge-2026,
automaticamente nos da el código `JEDI-XXXX` generado por la aplicación, y con ese codigo se accede a el juego

### Inicio rápido con Docker

```powershell
cd app-v2
Copy-Item .env.example .env
docker compose up --build
```

Abre <http://localhost:8501>. Antes de usar la aplicación, cambia en `.env` la
contraseña de `MLFLOW_JEDI_TEACHER_PASSWORD`.

Para detenerla sin perder los datos:

```powershell
docker compose down
```

La guía completa de instalación, uso y pruebas está en el
[`README de app-v2`](app-v2/README.md).

## Material docente

### Para el alumnado

- [`Misiones_ALUMNADO_DIGITS.docx`](docs/alumnado/Misiones_ALUMNADO_DIGITS.docx):
  fichas de misiones y holocrones.

### Para el profesorado

- [`Guion_PROFESORAS_DIGITS.docx`](docs/profesorado/Guion_PROFESORAS_DIGITS.docx):
  guía para preparar e impartir la sesión.
- [`Misiones_PROFESORADO_DIGITS.docx`](docs/profesorado/Misiones_PROFESORADO_DIGITS.docx):
  guía de corrección de las misiones.
- [`Guía rápida de la aplicación`](app-v2/docs/GUIA_PROFESORADO.md): dinámica,
  puntuación y actuación durante la actividad.
- [`Guía de mantenimiento`](app-v2/docs/GUIA_MANTENIMIENTO.md): persistencia,
  copias de seguridad y actualizaciones.

### Referencia

- [`Resumen_Manual_MLflow.docx`](docs/referencia/Resumen_Manual_MLflow.docx):
  resumen teórico.
- [`Guia_estructura_pildora_extendida.pdf`](docs/referencia/Guia_estructura_pildora_extendida.pdf)
  y [`MLflow_Jedi_Library.pdf`](docs/referencia/MLflow_Jedi_Library.pdf): fuentes
  de consulta.

## Notebooks

### Live coding

- [`Live_Coding_COMPLETO.ipynb`](notebooks/01_live_coding/Live_Coding_COMPLETO.ipynb):
  versión completa de consulta.
- [`Live_Coding_DEMO_SEGURA.ipynb`](notebooks/01_live_coding/Live_Coding_DEMO_SEGURA.ipynb):
  versión recomendada para la exposición.
- [`Live_Coding_PARA_RELLENAR.ipynb`](notebooks/01_live_coding/Live_Coding_PARA_RELLENAR.ipynb):
  versión con huecos para practicar.

### Práctica

- [`01_Tracking_Ejercicios.ipynb`](notebooks/02_practica/01_Tracking_Ejercicios.ipynb):
  ejercicios iniciales.
- [`02_Archivos_Jedi_SOLUCION.ipynb`](notebooks/02_practica/02_Archivos_Jedi_SOLUCION.ipynb):
  solución completa.
- [`03_Orden_66_RETO.ipynb`](notebooks/02_practica/03_Orden_66_RETO.ipynb):
  reto final para el alumnado.

## Estructura

```text
.
├── app-v2/       # aplicación Streamlit, pruebas y documentación operativa
├── assets/       # imágenes de apoyo para el material docente
├── docs/         # documentos para alumnado, profesorado y referencia
└── notebooks/    # live coding y prácticas
```

Los documentos y notebooks de la raíz se mantienen como material complementario
y como alternativa si no es posible utilizar la aplicación durante la sesión.
