import streamlit as st
import uuid
from supabase import create_client, Client

# Configura tus credenciales de Supabase (ideal usar st.secrets)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="Face detection",
    page_icon=":guardsman:",
)
st.title("Formulario de Datos Personales")
st.sidebar.success("select a page above.")

if 'show_camera' not in st.session_state:
    st.session_state.show_camera = False
if 'captured_image' not in st.session_state:
    st.session_state.captured_image = None
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

with st.form("datos_personales"):
    nombre = st.text_input("Nombre completo")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    CC = st.text_input("C.C")
    correo = st.text_input("Correo electrónico")
    genero = st.selectbox("Género", ["Selecciona...", "Masculino", "Femenino", "Otro"])

    col1, col2 = st.columns(2)
    with col1:
        if st.form_submit_button("📸 Activar cámara"):
            st.session_state.show_camera = True
            st.session_state.uploaded_image = None
    with col2:
        upload_image = st.file_uploader(
            "⬆️ Subir imagen",
            type=["jpg", "jpeg", "png"],
            help="Formatos permitidos: JPG, JPEG, PNG",
            key="file_uploader"
        )
        if upload_image:
            st.session_state.uploaded_image = {
                "bytes": upload_image.getvalue(),
                "filename": upload_image.name
            }
            st.session_state.captured_image = None
            st.session_state.show_camera = False

    if st.session_state.show_camera:
        camera_input = st.camera_input("Toma tu foto")
        if camera_input:
            st.session_state.captured_image = {
                "bytes": camera_input.getvalue(),
                "filename": f"camera_{uuid.uuid4().hex}.png"
            }
            st.session_state.show_camera = False

    enviar = st.form_submit_button("✅ Enviar")

    if enviar:
        campos_vacios = (
            not nombre.strip() or
            edad == 0 or
            not CC.strip() or
            not correo.strip() or
            genero == "Selecciona..."
        )
        if campos_vacios:
            st.error("❌ Por favor, completa todos los campos obligatorios.")
        else:
            # Seleccionar imagen
            imagen_data = st.session_state.captured_image or st.session_state.uploaded_image

            # Subir imagen a Supabase Storage
            imagen_url = None
            if imagen_data:
                # Crear un nombre único para la imagen
                unique_filename = f"{uuid.uuid4().hex}_{imagen_data['filename']}"
                try:
                    res = supabase.storage.from_("validaciones").upload(unique_filename, imagen_data["bytes"])
                    if res.get("error") is None:
                        # Obtener URL pública
                        imagen_url = supabase.storage.from_("validaciones").get_public_url(unique_filename).get("publicUrl")
                    else:
                        st.error(f"Error subiendo imagen: {res['error']['message']}")
                except Exception as e:
                    st.error(f"Error subiendo imagen: {e}")

            # Insertar datos en la tabla
            try:
                data = {
                    "nombre": nombre,
                    "edad": edad,
                    "cc": CC,
                    "correo": correo,
                    "genero": genero,
                    "imagen_url": imagen_url,
                }
                insert_resp = supabase.table("datos_personales").insert(data).execute()
                if response.status_code != 201:  # 201 Created al insertar
                    st.error(f"Error guardando datos: {response.error}")
                else:
                    st.success("Datos guardados correctamente")

            except Exception as e:
                st.error(f"Error guardando datos: {e}")

            # Resetear estados después del éxito
            st.session_state.captured_image = None
            st.session_state.uploaded_image = None
