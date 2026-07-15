# MLflow Jedi · La Cámara de los Experimentos Perdidos

Nueva aplicación práctica de la píldora extendida. Los documentos y notebooks de la raíz del repositorio se conservan como plan de contingencia.

## Qué incluye

- acceso sin cuentas mediante código de sesión y nombre de equipo;
- seis cámaras didácticas con validación AST y feedback conceptual;
- tres misiones reales de Random Forest sobre Digits;
- tracking real con MLflow: 5 parámetros, 4 métricas, 2 artefactos y 1 modelo;
- comparador de runs y métricas por clase;
- siete holocrones, formulario y tarjeta de defensa;
- panel docente con seguimiento, pistas, desbloqueos, reinicios y reasignación;
- exportación JSON/CSV y persistencia SQLite;
- empaquetado Docker con volumen persistente.

## Ejecución local

1. Copia `.env.example` como `.env` y cambia la contraseña docente.
2. Crea un entorno de Python 3.12 e instala `pip install -r requirements.txt`.
3. Ejecuta `streamlit run app.py`.
4. Abre `http://localhost:8501`.

## Docker

```bash
docker compose up --build
```

El volumen `mlflow_jedi_data` conserva sesiones, runs, modelos y artefactos aunque el contenedor se reinicie.

## Seguridad

El texto introducido por el alumnado nunca se ejecuta. Se analiza con `ast`, se rechazan imports y llamadas no autorizadas, y una plantilla interna controlada realiza el entrenamiento real.

## Contingencia

Si la aplicación o la conexión fallan, utiliza los notebooks y documentos conservados en las carpetas `notebooks/` y `docs/` de la raíz del repositorio.

## Despliegue

No se ha elegido proveedor. La aplicación queda preparada para un servidor con Docker y volumen persistente; la decisión de alojamiento se tomará después de validar la experiencia local.
