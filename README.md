# 🤖 FiberBot AI

FiberBot AI es un agente de inteligencia artificial desarrollado para el **Challenge Alura Agentes**, especializado en consultas técnicas relacionadas con redes de fibra óptica.

El sistema utiliza una arquitectura **RAG (Retrieval-Augmented Generation)** para recuperar información relevante desde documentación técnica y utilizarla como contexto para generar respuestas mediante inteligencia artificial.

## 🌐 Aplicación desplegada

FiberBot AI se encuentra disponible públicamente en:

https://fiberbot-ai.streamlit.app

## 🎯 Objetivo

Facilitar a los colaboradores la consulta de información contenida en documentos técnicos de fibra óptica mediante una interfaz conversacional sencilla.

En lugar de buscar manualmente información dentro de diferentes documentos, el usuario puede realizar preguntas en lenguaje natural y FiberBot AI recuperará los fragmentos más relevantes para construir una respuesta.

## 🧠 Arquitectura

FiberBot AI utiliza una arquitectura RAG:

```text
Usuario
   ↓
Pregunta
   ↓
Embedding
   ↓
FAISS
   ↓
Búsqueda semántica
   ↓
Fragmentos relevantes
   ↓
Gemini
   ↓
Respuesta
```

### Flujo de funcionamiento

1. El usuario realiza una pregunta.
2. La pregunta se transforma en un embedding.
3. FAISS realiza una búsqueda semántica dentro de la base vectorial.
4. Se recuperan los fragmentos de documentos más relacionados con la consulta.
5. Los fragmentos recuperados son enviados como contexto al modelo Gemini.
6. Gemini genera una respuesta utilizando la información recuperada.
7. La respuesta se muestra progresivamente en la interfaz.

## 🛠️ Tecnologías utilizadas

- Python
- Streamlit
- Google Gemini API
- FAISS
- Embeddings
- Arquitectura RAG
- Git y GitHub
- Streamlit Community Cloud

## 📚 Base de conocimiento

La base de conocimiento utilizada por FiberBot AI contiene documentación relacionada con diferentes aspectos técnicos de redes de fibra óptica, incluyendo:

- Construcción de redes
- Seguridad
- Tecnología GPON
- Preguntas frecuentes

Los documentos son procesados previamente para generar fragmentos y representaciones vectoriales que posteriormente pueden ser consultadas mediante búsqueda semántica.

## 🗂️ Estructura del proyecto

```text
FiberBot-AI/
│
├── assets/
│   ├── fiberbot_header.png
│   └── fiberbot_deploy.png
│
├── documentos/
│   └── Documentación técnica
│
├── src/
│   ├── buscador.py
│   ├── chatbot.py
│   └── embeddings.py
│
├── interfaz.py
├── preparar_base.py
├── fragmentos.json
├── indice_faiss.index
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/Miguelena93/FiberBot-AI.git
cd FiberBot-AI
```

### 2. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar Gemini API

Crear un archivo `.env` en la raíz del proyecto:

```env
GEMINI_API_KEY=TU_API_KEY
```

> La API Key no debe almacenarse públicamente en GitHub.

### 4. Ejecutar FiberBot AI

```bash
python -m streamlit run interfaz.py
```
## 💬 Ejemplos de uso

FiberBot AI puede responder preguntas relacionadas con la documentación técnica incorporada en su base de conocimiento.

### Ejemplo 1

**Pregunta:**

> ¿Cuáles son las medidas de seguridad que debo seguir al realizar trabajos de fibra óptica?

**Respuesta:**

FiberBot AI recupera información relevante de los documentos técnicos y proporciona medidas y lineamientos de seguridad aplicables a trabajos de construcción, mantenimiento e instalación de redes de fibra óptica.

### Otras preguntas que puede responder

- ¿Qué medidas de seguridad deben aplicarse durante la instalación de fibra óptica?
- ¿Qué es una red GPON?
- ¿Cuáles son los principales componentes de una red de fibra óptica?
- ¿Qué recomendaciones deben seguirse durante trabajos de construcción de redes?
- ¿Qué procedimientos técnicos aparecen en los manuales disponibles?

Las respuestas son generadas utilizando los fragmentos relevantes recuperados de la base documental mediante búsqueda semántica.

## ☁️ Deploy

La aplicación fue desplegada utilizando **Streamlit Community Cloud** y se encuentra conectada al repositorio público de GitHub.

La API Key de Gemini se administra mediante el sistema de **Secrets** de Streamlit, evitando exponer credenciales dentro del código fuente.

## 📸 FiberBot AI funcionando en la nube

![FiberBot AI ejecutándose en Streamlit Cloud](assets/FiberBot AI_deploy.png)

La imagen anterior muestra FiberBot AI ejecutándose desde su URL pública y respondiendo una consulta técnica utilizando su base de conocimiento.

## 🔐 Seguridad

Las credenciales utilizadas por el proyecto no se almacenan en el repositorio.

El archivo `.env` se encuentra excluido mediante `.gitignore` y las credenciales utilizadas durante el despliegue se administran mediante variables de entorno/Secrets.

## 💡 Funcionalidades

- Interfaz conversacional
- Historial de conversación durante la sesión
- Búsqueda semántica
- Recuperación de contexto mediante FAISS
- Generación de respuestas con Gemini
- Respuestas progresivas mediante streaming
- Base de conocimiento documental
- Opción para limpiar la conversación
- Interfaz personalizada para FiberBot AI
- Aplicación desplegada públicamente

## 👨‍💻 Autor

Desarrollado por **Miguelena93** para el Challenge **Alura Agentes**.

## 🏆 Challenge Alura Agentes

Proyecto desarrollado como parte del desafío de Inteligencia Artificial de **Alura Latam**, aplicando conceptos de agentes de IA, embeddings, recuperación de información, modelos generativos y arquitectura RAG.