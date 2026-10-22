import os
import streamlit as st
from google import genai

# Configuración de la página de Streamlit
st.set_page_config(page_title="Entrevista IA", page_icon="🤖")

st.title("🎤 Entrevista con IA")

# 1. Obtener la clave de API de forma segura (compatible con Streamlit Cloud y entorno local)
api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ No se encontró la `GEMINI_API_KEY`. Configúrala en los Secrets de Streamlit o como variable de entorno.")
    st.stop()

# 2. Inicializar el cliente de Gemini
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Error al inicializar el cliente de Gemini: {e}")
    st.stop()

# Define el ID del modelo (asegúrate de que esté activo y sea correcto)
MODEL_ID = "gemini-2.5-flash"  # O puedes cambiarlo a "gemini-1.5-flash"

# Ejemplo de interfaz o lógica de tu entrevista
st.write("¡Bienvenido a la entrevista! Responde a la siguiente pregunta:")

prompt_usuario = st.text_input("Escribe tu respuesta aquí:")

if st.button("Enviar respuesta"):
    if prompt_usuario.strip():
        try:
            # 3. Llamada segura con manejo de excepciones para ver el error real
            with st.spinner("Generando respuesta de la IA..."):
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=prompt_usuario,
                )
            
            st.success("Respuesta de la IA:")
            st.write(response.text)
            
        except Exception as e:
            # Esto mostrará el error exacto (por ejemplo, cuotas excedidas, modelo inválido, etc.)
            st.error(f"❌ Ocurrió un error en la API de Gemini: {e}")
    else:
        st.warning("Por favor, escribe un mensaje antes de enviar.")

# Botón de reinicio opcional
if st.button("Reiniciar Entrevista"):
    st.rerun()