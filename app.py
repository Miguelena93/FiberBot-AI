from google import genai
from dotenv import load_dotenv
import os
import json
import faiss

from src.embeddings import generar_embedding
from src.buscador import buscar_fragmentos
from src.chatbot import generar_respuesta


load_dotenv()

cliente = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Cargar fragmentos
with open(
    "fragmentos.json",
    "r",
    encoding="utf-8"
) as archivo:

    fragmentos = json.load(archivo)


# Cargar índice FAISS ya creado
indice_faiss = faiss.read_index(
    "indice_faiss.index"
)


print("=" * 50)
print("🤖 FIBERBOT AI")
print("=" * 50)

print(
    "\nHola 👋 Soy FiberBot AI, "
    "tu asistente técnico especializado en fibra óptica."
)

print(
    "Puedes preguntarme sobre Tecnología GPON, Sobre construcción de Red GPON, "
    "Instalación y Seguridad en Campo."
)

print("\nEscribe 'salir' para finalizar.\n")


while True:

    pregunta = input("Tú: ")

    if pregunta.lower().strip() == "salir":
        print(
            "\nFiberBot: ¡Hasta luego! 👋 "
            "Trabaja siempre con seguridad."
        )
        break

    embedding_pregunta = generar_embedding(
        cliente,
        pregunta
    )

    resultados = buscar_fragmentos(
        indice_faiss,
        embedding_pregunta,
        fragmentos,
        cantidad=5
    )

    respuesta = generar_respuesta(
        cliente,
        pregunta,
        resultados
    )

    print(f"\nFiberBot: {respuesta}\n")