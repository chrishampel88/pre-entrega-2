
import os

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from pydantic import ValidationError

from schemas import ExtraccionTecnica

# Cargamos las variables del archivo .env
load_dotenv()


# Creamos el prompt con LangChain
prompt = ChatPromptTemplate.from_messages([
    ("system", """Analizá el texto técnico y extraé:
    - Las tecnologías mencionadas.
    - La criticidad: baja, media o alta.
    - Un resumen técnico breve en español.

    No inventes tecnologías."""),

    ("human", "Texto para analizar:\n{texto}")
])


# Contador para observar los intentos
intentos = 0


def registrar_intento(entrada: dict) -> dict:
    global intentos

    intentos += 1
    print(f"[INFO] Intento número {intentos}")

    return entrada


# Validamos la respuesta del modelo
def validar_salida(resultado: dict) -> ExtraccionTecnica:

    raw = resultado["raw"]

    # Comprobamos si la respuesta quedó incompleta
    finish_reason = raw.response_metadata.get("finish_reason")

    if finish_reason in ("length", "max_tokens"):
        raise ValueError("Respuesta incompleta por límite de tokens")

    # Comprobamos errores al interpretar la respuesta
    if resultado["parsing_error"] is not None:
        raise ValueError("Respuesta mal formada o inválida")

    parsed = resultado["parsed"]

    if parsed is None:
        raise ValueError("El modelo no devolvió un objeto válido")

    # Validamos utilizando Pydantic
    return ExtraccionTecnica.model_validate(parsed)


# Creamos nuestra cadena LCEL
def crear_cadena():

    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Falta OPENAI_API_KEY en .env")

    modelo = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        max_tokens=500,
        timeout=30
    )

    cadena = (
        RunnableLambda(registrar_intento)
        | prompt
        | modelo.with_structured_output(
            ExtraccionTecnica,
            include_raw=True
        )
        | RunnableLambda(validar_salida)
    )

    # Permitimos hasta 2 intentos en total
    return cadena.with_retry(
        retry_if_exception_type=(ValueError, ValidationError),
        stop_after_attempt=2,
        wait_exponential_jitter=False
    )


# Función asíncrona principal
async def process_text(text: str):

    global intentos
    intentos = 0

    print("[INFO] Iniciando procesamiento")

    try:

        # Creamos la cadena
        chain = crear_cadena()

        # Ejecutamos de forma asíncrona
        resultado = await chain.ainvoke({"texto": text})

        print("[INFO] Respuesta recibida y validada")

        return resultado

    except Exception as error:

        print("[ERROR] No se pudo procesar el texto:", error)

        return None
