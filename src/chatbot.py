from google import genai


MODELO_CHAT = "gemini-3.5-flash-lite"


def construir_prompt(
    pregunta: str,
    fragmentos_encontrados: list[str]
) -> str:
    """
    Construye el prompt que utilizará FiberBot.
    """

    contexto = "\n\n---\n\n".join(
        fragmentos_encontrados
    )

    prompt = f"""
Eres FiberBot AI, un asistente técnico profesional
especializado en fibra óptica.

Responde la pregunta utilizando únicamente la información
proporcionada en el contexto.

Si la respuesta no se encuentra en el contexto, indica claramente
que no tienes suficiente información para responder.

No menciones números de preguntas, números de FAQ ni referencias
como "Pregunta 59".

No incluyas números de sección dentro de los títulos
de la respuesta.

Redacta la respuesta de forma clara, profesional y natural.

CONTEXTO:
{contexto}

PREGUNTA:
{pregunta}

RESPUESTA:
"""

    return prompt


def generar_respuesta(
    cliente: genai.Client,
    pregunta: str,
    fragmentos_encontrados: list[str]
) -> str:
    """
    Genera una respuesta completa.
    """

    prompt = construir_prompt(
        pregunta,
        fragmentos_encontrados
    )

    respuesta = cliente.models.generate_content(
        model=MODELO_CHAT,
        contents=prompt
    )

    return respuesta.text


def generar_respuesta_stream(
    cliente: genai.Client,
    pregunta: str,
    fragmentos_encontrados: list[str]
):
    """
    Genera la respuesta progresivamente para mostrarla
    en tiempo real en la interfaz.
    """

    prompt = construir_prompt(
        pregunta,
        fragmentos_encontrados
    )

    respuesta_stream = cliente.models.generate_content_stream(
        model=MODELO_CHAT,
        contents=prompt
    )

    for fragmento in respuesta_stream:

        if fragmento.text:
            yield fragmento.text