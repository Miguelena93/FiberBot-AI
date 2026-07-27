import faiss
import numpy as np


def crear_indice_faiss(
    embeddings: list[list[float]]
) -> faiss.IndexFlatL2:
    """
    Crea un índice FAISS usando los embeddings recibidos.
    """

    if not embeddings:
        raise ValueError("No hay embeddings para crear el índice.")

    matriz_embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    dimensiones = matriz_embeddings.shape[1]

    indice = faiss.IndexFlatL2(dimensiones)

    indice.add(matriz_embeddings)

    return indice

def buscar_fragmentos(
    indice,
    embedding_pregunta: list[float],
    fragmentos: list[str],
    cantidad: int = 5
) -> list[str]:
    """
    Busca los fragmentos más cercanos a la pregunta.
    """

    vector_pregunta = np.array(
        [embedding_pregunta],
        dtype="float32"
    )

    distancias, indices = indice.search(
        vector_pregunta,
        cantidad
    )

    resultados = []

    for posicion in indices[0]:
        resultados.append(fragmentos[posicion])

    return resultados