from google import genai
from google.genai import types
import time

MODELO_EMBEDDING = "gemini-embedding-2"
DIMENSIONES = 768


def generar_embedding(
    cliente: genai.Client,
    texto: str
) -> list[float]:
    """
    Genera el embedding de un único fragmento.
    """

    if not texto.strip():
        raise ValueError("El texto está vacío.")

    respuesta = cliente.models.embed_content(
        model=MODELO_EMBEDDING,
        contents=texto,
        config=types.EmbedContentConfig(
            output_dimensionality=DIMENSIONES
        )
    )

    return respuesta.embeddings[0].values


def generar_embeddings(
    cliente: genai.Client,
    fragmentos: list[str]
) -> list[list[float]]:
    """
    Genera los embeddings de todos los fragmentos.
    """

    if not fragmentos:
        raise ValueError("La lista de fragmentos está vacía.")

    embeddings = []


    total = len(fragmentos)

    for indice, fragmento in enumerate(fragmentos, start=1):

        print(f"Generando embedding {indice}/{total}...")

        embedding = generar_embedding(
            cliente,
            fragmento
        )

        embeddings.append(embedding)

        # Evitamos pasar el límite gratuito de Gemini
        if indice % 90 == 0 and indice < total:
            print("\n⏳ Esperando 60 segundos para continuar...\n")
            time.sleep(60)

    return embeddings