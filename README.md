# Pre-entrega 2 - Pipeline de procesamiento validado

Proyecto de AI Engineering para extraer información técnica de un texto mediante LangChain (LCEL), OpenAI y Pydantic.

## ¿Qué hace?

Recibe una descripción técnica o un log de error y devuelve tres datos validados:

- `tecnologias`: lista de tecnologías mencionadas en el texto.
- `nivel_de_criticidad`: `baja`, `media` o `alta`.
- `resumen_tecnico`: breve descripción del problema o sistema.

## Archivos del proyecto

- `schemas.py`: define y valida los campos de salida con Pydantic.
- `chain.py`: contiene el prompt, el modelo de OpenAI, la cadena LCEL y los reintentos.
- `main.py`: ejecuta una prueba asíncrona con un texto de ejemplo.
- `.env.example`: muestra las variables de entorno necesarias.
- `requirements.txt`: dependencias del proyecto.
- `.gitignore`: excluye las claves y archivos temporales.

## Instalación

La consigna indica Python 3.12. Desde Git Bash, dentro de la carpeta del proyecto:

```bash
py -3.12 -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
```

Si estás usando Python 3.13, podés crear el entorno con `py -3.13 -m venv .venv`, aunque la versión solicitada por el curso es 3.12.

## Variables de entorno

Creá un archivo `.env` a partir de `.env.example`:

```dotenv
OPENAI_API_KEY=tu_clave_de_openai
OPENAI_MODEL=gpt-4o-mini
```

No subas `.env` a GitHub: contiene una clave privada.

## Ejecución

Con el entorno virtual activado, ejecutá:

```bash
python main.py
```

El programa usa una llamada real a OpenAI, por lo que necesitás una API key con créditos disponibles. Para probar otro caso, cambiá el texto de ejemplo en `main.py`.

## ¿Cómo funciona?

La cadena LCEL conecta el prompt, el modelo y la salida estructurada con Pydantic:

```python
cadena = prompt | modelo.with_structured_output(ExtraccionTecnica)
```

La implementación también comprueba si hubo problemas al interpretar la respuesta o si quedó incompleta por el límite de tokens. Se utiliza `.with_retry()` para permitir hasta **dos intentos en total** cuando ocurre un error de validación.

La función asíncrona `process_text(text)` ejecuta la cadena mediante `.ainvoke()`.

## Mensajes en la terminal

Usamos `print()` para mostrar mensajes sencillos de seguimiento, sin la librería `logging`:

```text
[INFO] Iniciando procesamiento
[INFO] Intento número 1
[INFO] Respuesta recibida y validada
```

Si el resultado no es válido, la cadena puede volver a intentarlo. Si falla definitivamente, se muestra un mensaje `[ERROR]`.

## Ejemplo de salida esperada

```json
{
  "tecnologias": ["FastAPI", "Redis", "PostgreSQL"],
  "nivel_de_criticidad": "alta",
  "resumen_tecnico": "API con caché en Redis y persistencia en PostgreSQL; problema con las conexiones concurrentes."
}
```

El contenido se genera a partir del texto recibido y puede variar. No es una respuesta fija.

## Limitaciones

- Si el texto no menciona tecnologías y el esquema exige al menos una, la validación puede fallar.
- Los reintentos no garantizan una respuesta válida y pueden consumir tokens adicionales.
- El manejo de reintentos está orientado a errores de validación, no a todos los errores de la API.
