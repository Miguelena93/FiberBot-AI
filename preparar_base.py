from google import genai
from dotenv import load_dotenv
import os
import json
import faiss
from pathlib import Path
from pypdf import PdfReader

from src.embeddings import generar_embeddings
from src.buscador import crear_indice_faiss


load_dotenv()

cliente = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

carpeta_documentos = Path("documentos")
archivos_pdf = list(carpeta_documentos.glob("*.pdf"))

texto_completo = ""

print("=" * 50)
print("PREPARANDO BASE DE CONOCIMIENTO DE FIBERBOT")
print("=" * 50)

# Leer PDFs
for archivo_pdf in archivos_pdf:
    print(f"Leyendo: {archivo_pdf.name}")

    reader = PdfReader(archivo_pdf)

    for numero_pagina, pagina in enumerate(reader.pages, start=1):
        texto_pagina = pagina.extract_text()

        if texto_pagina:
            texto_completo += (
                f"\n\nDOCUMENTO: {archivo_pdf.name}\n"
                f"PÁGINA: {numero_pagina}\n"
                f"{texto_pagina}"
            )

# Crear fragmentos
tamano_fragmento = 1000
fragmentos = []

for inicio in range(0, len(texto_completo), tamano_fragmento):
    fragmento = texto_completo[
        inicio:inicio + tamano_fragmento
    ]

    fragmentos.append(fragmento)

print(f"\nFragmentos creados: {len(fragmentos)}")

# Guardar fragmentos
with open(
    "fragmentos.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        fragmentos,
        archivo,
        ensure_ascii=False,
        indent=4
    )

print("✅ Fragmentos guardados")

# Generar embeddings
print("\nGenerando embeddings...")

embeddings = generar_embeddings(
    cliente,
    fragmentos
)

# Crear índice FAISS
print("\nCreando índice FAISS...")

indice_faiss = crear_indice_faiss(
    embeddings
)

# Guardar índice FAISS
faiss.write_index(
    indice_faiss,
    "indice_faiss.index"
)

print("\n✅ BASE DE CONOCIMIENTO CREADA")
print(f"Vectores almacenados: {indice_faiss.ntotal}")
print("✅ Índice guardado en indice_faiss.index")