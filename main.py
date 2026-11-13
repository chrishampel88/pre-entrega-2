import asyncio
import logging

from chain import process_text

# Mostramos los logs del pipeline en la terminal.
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

TEXTO = (
    "Nuestra API usa FastAPI, Redis y PostgreSQL. "
    "Hay errores de conexión a la base de datos bajo mucha carga "
    "y el servicio deja de responder a los usuarios."
)


async def main():
    try:
        resultado = await process_text(TEXTO)
        print("\nRESULTADO JSON:")
        print(resultado.model_dump_json(indent=2))
    except Exception as error:
        logging.error("No se pudo procesar el texto: %s", error)


if __name__ == "__main__":
    asyncio.run(main())
