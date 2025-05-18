import streamlit as st

# Configuración principal de la aplicación
st.set_page_config(
    page_title="Sistema de Reconocimiento Facial",
    page_icon="👤",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Página principal
st.title("Bienvenido al Sistema de Reconocimiento Facial 👤")
st.markdown("""
    **Selecciona una opción en el menú lateral para:**
    - 🖋️ Registrar nuevos usuarios
    - 📷 Validar acceso mediante reconocimiento facial
""")

st.sidebar.title("Navegación")
st.sidebar.success("Selecciona una página del menú superior.")

# Información adicional en la página principal
st.divider()
st.subheader("Instrucciones de uso:")
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        **Registro de usuarios:**
        1. Completa el formulario
        2. Toma una foto o sube una imagen
        3. Envía los datos
    """)

with col2:
    st.markdown("""
        **Validación de acceso:**
        1. Abre la cámara
        2. Toma una foto
        3. Espera la verificación
    """)

st.divider()
st.markdown("> Sistema desarrollado con Streamlit 🚀 | © 2024")