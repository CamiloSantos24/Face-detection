import streamlit as st
import os
import csv
import uuid

st.set_page_config(
    page_title="Face detection",
    page_icon=":guardsman:",    
)
st.title("Formulario de Datos Personales")
st.sidebar.success("select a page above.")

# Estados para manejar ambas fuentes de imagen
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

    # Sección de imagen (cámara o upload)
    col1, col2 = st.columns(2)
    with col1:
        if st.form_submit_button("📸 Activar cámara"):
            st.session_state.show_camera = True
            st.session_state.uploaded_image = None  # Resetear upload si usan cámara

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
            st.session_state.captured_image = None  # Resetear cámara si suben archivo
            st.session_state.show_camera = False

    # Mostrar cámara solo si está activada
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
            # Crear carpeta si no existe
            datos_dir = os.path.join(os.getcwd(), "datos")
            os.makedirs(datos_dir, exist_ok=True)

            # Determinar qué imagen usar
            imagen_data = None
            if st.session_state.captured_image:
                imagen_data = st.session_state.captured_image
            elif st.session_state.uploaded_image:
                imagen_data = st.session_state.uploaded_image

            # Guardar datos en CSV
            datos_path = os.path.join(datos_dir, "datos_personales.csv")
            file_exists = os.path.isfile(datos_path)
            
            with open(datos_path, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Nombre", "Edad", "C.C", "Correo", "Género", "Imagen"])
                
                imagen_nombre = imagen_data["filename"] if imagen_data else ""
                writer.writerow([nombre, edad, CC, correo, genero, imagen_nombre])

            # Guardar imagen si existe
            if imagen_data:
                imagen_path = os.path.join(datos_dir, imagen_data["filename"])
                with open(imagen_path, "wb") as img_file:
                    img_file.write(imagen_data["bytes"])

            # Mensaje de éxito
            mensaje = (
                f"¡Datos guardados correctamente! 🎉\n\n"
                f"**Nombre:** {nombre}\n"
                f"**Edad:** {edad}\n"
                f"**CC:** {CC}\n"
                f"**Correo:** {correo}\n"
                f"**Género:** {genero}"
            )
            
            if imagen_data:
                mensaje += f"\n\n**Imagen guardada:** `{imagen_data['filename']}`"
                if st.session_state.captured_image:
                    mensaje += " (desde cámara)"
                else:
                    mensaje += " (desde archivo)"

            st.success(mensaje)

            # Resetear estados después del éxito
            st.session_state.captured_image = None
            st.session_state.uploaded_image = None