import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import json
import faiss

from src.embeddings import generar_embedding
from src.buscador import buscar_fragmentos
from src.chatbot import generar_respuesta_stream


# ==========================================
# CONFIGURACIÓN GENERAL
# ==========================================

st.set_page_config(
    page_title="FiberBot AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

load_dotenv()


# ==========================================
# CLIENTE GEMINI
# ==========================================

@st.cache_resource
def crear_cliente():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(
        api_key=api_key
    )


cliente = crear_cliente()

if cliente is None:
    st.error("❌ No se encontró la API Key de Gemini.")
    st.stop()


# ==========================================
# BASE DE CONOCIMIENTO
# ==========================================

@st.cache_resource
def cargar_base():

    with open(
        "fragmentos.json",
        "r",
        encoding="utf-8"
    ) as archivo:

        fragmentos = json.load(archivo)

    indice_faiss = faiss.read_index(
        "indice_faiss.index"
    )

    return fragmentos, indice_faiss


fragmentos, indice_faiss = cargar_base()


# ==========================================
# ESTILOS
# ==========================================

st.markdown(
    """
    <style>

    /* ======================================
       FONDO GENERAL
       ====================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 50% 0%,
                rgba(20, 96, 190, 0.18),
                transparent 35%
            ),
            linear-gradient(
                180deg,
                #061426 0%,
                #071a30 55%,
                #050f1d 100%
            ) !important;

        color: #f4f7fb;
    }


    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: transparent !important;
    }


    [data-testid="stHeader"] {
        background: #061426 !important;
    }


    /* ======================================
       ÁREA PRINCIPAL
       ====================================== */

    .block-container {
        max-width: 900px;
        padding-top: 7rem;
        padding-bottom: 11rem;
    }


    /* ======================================
       ENCABEZADO FIJO
       ====================================== */

    .st-key-fiberbot_header {
        position: fixed;

        top: 3.2rem;
        left: 50%;
        transform: translateX(-50%);

        width: min(900px, calc(100vw - 2rem));

        z-index: 1000;

        background: rgba(5, 18, 34, 0.96);

        backdrop-filter: blur(12px);

        padding-top: 0.8rem;
        padding-bottom: 0.8rem;

        border-bottom:
            1px solid rgba(45, 135, 255, 0.30);
    }


    .st-key-fiberbot_header h1 {
        text-align: center;

        margin: 0;
        padding: 0;

        color: #ffffff;

        text-shadow:
            0 0 18px rgba(35, 137, 255, 0.25);
    }


    .fiberbot-subtitle {
        text-align: center;

        color: #8fb9e8;

        font-size: 1rem;

        margin-top: 0.3rem;
        margin-bottom: 0;
    }


    /* ======================================
       BANNER
       ====================================== */

    .st-key-banner_fiberbot img {
        border-radius: 16px;

        border:
            1px solid rgba(55, 135, 255, 0.20);

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.20);
    }


    /* ======================================
       MENSAJES
       ====================================== */

    div[data-testid="stChatMessage"] {
        background:
            rgba(14, 38, 66, 0.82);

        border:
            1px solid rgba(57, 139, 255, 0.18);

        border-radius: 16px;

        padding: 0.8rem 1rem;

        margin-bottom: 0.8rem;
    }


    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] li,
    div[data-testid="stChatMessage"] strong,
    div[data-testid="stChatMessage"] span {
        color: #edf4ff !important;
    }


    /* ======================================
       ZONA INFERIOR DEL INPUT
       ====================================== */

    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    [data-testid="stBottomBlockContainer"],
    [data-testid="stChatFloatingInputContainer"],
    [data-testid="stChatInputContainer"],
    .stChatFloatingInputContainer,
    .stChatInputContainer {

        background: #061426 !important;
        background-color: #061426 !important;

        box-shadow: none !important;
    }


    [data-testid="stBottomBlockContainer"] {
        bottom: 72px !important;
        z-index: 999 !important;
    }


    [data-testid="stBottomBlockContainer"] > div {
        max-width: 900px !important;

        margin-left: auto !important;
        margin-right: auto !important;
    }


    /* ======================================
       CAJA DE ESCRITURA
       ====================================== */

        /* Texto escrito dentro del chat input */
    [data-testid="stChatInput"] textarea {
        color: #0b1f35 !important;
        -webkit-text-fill-color: #0b1f35 !important;
        caret-color: #1677ff !important;
        background: #eef3f9 !important;
    }

    /* Placeholder */
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6f8299 !important;
        -webkit-text-fill-color: #6f8299 !important;
        opacity: 1 !important;
    }

    /* Fondo completo del input */
    [data-testid="stChatInput"] {
        background: #eef3f9 !important;
        border: 1px solid rgba(66, 146, 255, 0.45) !important;
        border-radius: 14px !important;
    }


    /* ======================================
       CONTROLES INFERIORES
       ====================================== */

    .st-key-controles_inferiores {
        position: fixed;

        bottom: 0;
        left: 0;

        width: 100%;

        z-index: 998;

        background:
            rgba(5, 17, 31, 0.99);

        border-top:
            1px solid rgba(45, 135, 255, 0.25);

        padding-top: 7px;
        padding-bottom: 8px;
    }


    .st-key-controles_inferiores > div {
        max-width: 900px;

        margin-left: auto;
        margin-right: auto;
    }


    /* ======================================
       BOTÓN LIMPIAR
       ====================================== */

    div.stButton > button {
        border-radius: 12px;

        border:
            1px solid rgba(54, 137, 255, 0.35);

        background:
            rgba(12, 38, 68, 0.90);

        color: #edf4ff !important;
    }


    div.stButton > button p {
        color: #edf4ff !important;
    }


    div.stButton > button:hover {
        border-color: #2f8cff;

        background:
            rgba(20, 61, 105, 0.95);
    }


    /* ======================================
       POPOVER "CÓMO FUNCIONA"
       ====================================== */

    /* Botón del popover */
    [data-testid="stPopover"] button {
        background: rgba(12, 38, 68, 0.90) !important;
        color: #edf4ff !important;

        border: 1px solid rgba(54, 137, 255, 0.35) !important;

        border-radius: 12px !important;
    }   

    /* Texto dentro del botón */
    [data-testid="stPopover"] button p,
    [data-testid="stPopover"] button span,
    [data-testid="stPopover"] button div {
        color: #edf4ff !important;
        -webkit-text-fill-color: #edf4ff !important;
    }

    /* Hover */
    [data-testid="stPopover"] button:hover {
        background: rgba(20, 61, 105, 0.95) !important;
        border-color: #2f8cff !important;
    }


    /* ======================================
       FOOTER
       ====================================== */

    .fiberbot-footer {
        text-align: center;

        color: #6988aa;

        font-size: 0.72rem;

        margin-top: 2px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# ENCABEZADO
# ==========================================

with st.container(
    key="fiberbot_header"
):

    st.title("🤖 FiberBot AI")

    st.markdown(
        """
        <div class="fiberbot-subtitle">
            Inteligencia aplicada a consultas técnicas de fibra óptica.
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# ESTADO
# ==========================================

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []


# ==========================================
# BANNER DE BIENVENIDA
# ==========================================

if not st.session_state.mensajes:

    with st.container(
        key="banner_fiberbot"
    ):

        columna1, columna2, columna3 = st.columns(
            [5, 5, 5]
        )

        with columna2:

            st.image(
                "assets/fiberbot_header.png",
                use_container_width=True
            )


# ==========================================
# MENSAJE INICIAL
# ==========================================

if not st.session_state.mensajes:

    with st.chat_message("assistant"):

        st.markdown(
            """
            ¡Hola! 👋 Soy **FiberBot AI**.

            Puedo ayudarte a consultar información técnica relacionada con fibra óptica.

            **¿Qué deseas saber?**
            """
        )


# ==========================================
# HISTORIAL
# ==========================================

for mensaje in st.session_state.mensajes:

    with st.chat_message(
        mensaje["rol"]
    ):

        st.markdown(
            mensaje["contenido"]
        )


# ==========================================
# INPUT
# ==========================================

pregunta = st.chat_input(
    "Escribe tu pregunta..."
)


# ==========================================
# PROCESAR PREGUNTA
# ==========================================

if pregunta:

    # Guardar pregunta
    st.session_state.mensajes.append(
        {
            "rol": "user",
            "contenido": pregunta
        }
    )


    # Mostrar pregunta
    with st.chat_message("user"):

        st.markdown(
            pregunta
        )


    # Generar respuesta
    with st.chat_message("assistant"):

        with st.spinner(
            "Consultando la base de conocimiento..."
        ):

            embedding_pregunta = generar_embedding(
                cliente,
                pregunta
            )


            resultados = buscar_fragmentos(
                indice_faiss,
                embedding_pregunta,
                fragmentos,
                cantidad=3
            )


        respuesta_completa = st.write_stream(
            generar_respuesta_stream(
                cliente,
                pregunta,
                resultados
            )
        )


    # Guardar respuesta
    st.session_state.mensajes.append(
        {
            "rol": "assistant",
            "contenido": respuesta_completa
        }
    )


    # Redibujar
    st.rerun()


# ==========================================
# CONTROLES INFERIORES
# ==========================================

with st.container(
    key="controles_inferiores"
):

    col_info, col_espacio, col_limpiar = st.columns(
        [3, 4, 1.5]
    )


    # --------------------------------------
    # CÓMO FUNCIONA
    # --------------------------------------

    with col_info:

        with st.popover(
            "ℹ️ ¿Cómo funciona FiberBot?"
        ):

            st.markdown(
                """
                **FiberBot AI utiliza una arquitectura RAG.**

                **🧠 Embedding**  
                Convierte la consulta en una representación matemática de su significado.

                **🔎 FAISS**  
                Busca los fragmentos más relacionados dentro de la base vectorial.

                **📚 Recuperación**  
                Selecciona la información más relevante de los documentos técnicos.

                **🤖 Gemini**  
                Utiliza ese contexto para generar una respuesta.

                **Flujo**

                `Pregunta → Embedding → FAISS → Contexto → Gemini → Respuesta`
                """
            )


    # --------------------------------------
    # LIMPIAR
    # --------------------------------------

    with col_limpiar:

        if st.button(
            "🗑️ Limpiar",
            use_container_width=True
        ):

            st.session_state.mensajes = []

            st.rerun()


    # --------------------------------------
    # FOOTER
    # --------------------------------------

    st.markdown(
        """
        <div class="fiberbot-footer">
            FiberBot AI • Gemini + FAISS + RAG
        </div>
        """,
        unsafe_allow_html=True
    )