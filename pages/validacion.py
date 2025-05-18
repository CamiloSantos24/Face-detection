import streamlit as st
import cv2
import os
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="Validación de ingreso",
    page_icon=":camera:",
)

st.title("Validación de Ingreso")
st.sidebar.success("Selecciona una página arriba.")

# Estado para controlar la cámara
if 'show_validation_camera' not in st.session_state:
    st.session_state.show_validation_camera = False

# Botón para activar la cámara
if st.button("🎥 Abrir Cámara de Validación"):
    st.session_state.show_validation_camera = True

# Mostrar cámara cuando está activada
if st.session_state.show_validation_camera:
    validation_photo = st.camera_input("Toma tu foto para validar acceso", key="validation_camera")
    
    if validation_photo:
        st.success("✅ Foto capturada correctamente")
        # st.balloons()  # Quitado para no mostrar globos

        # --- Lógica de validación facial con OpenCV ---
        datos_dir = os.path.join(os.getcwd(), "datos")
        if not os.path.exists(datos_dir):
            st.error("No hay base de datos de imágenes para comparar.")
        else:
            # Convertir la imagen capturada a formato OpenCV
            img_pil = Image.open(validation_photo)
            img_np = np.array(img_pil.convert('RGB'))
            img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            # Cargar el clasificador de rostros de OpenCV
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img_cv, scaleFactor=1.1, minNeighbors=5)

            if len(faces) == 0:
                st.error("No se detectó ningún rostro en la foto capturada.")
                st.session_state.show_validation_camera = False
                st.stop()

            # Comparar con imágenes de la base de datos usando histogramas
            match_found = False
            for archivo in os.listdir(datos_dir):
                if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
                    ruta = os.path.join(datos_dir, archivo)
                    db_img = cv2.imread(ruta)
                    if db_img is None:
                        continue
                    db_img = cv2.resize(db_img, (img_cv.shape[1], img_cv.shape[0]))
                    # Comparar histogramas de color
                    hist1 = cv2.calcHist([img_cv], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
                    hist2 = cv2.calcHist([db_img], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
                    cv2.normalize(hist1, hist1)
                    cv2.normalize(hist2, hist2)
                    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                    if similarity > 0.10:  # Puedes ajustar el umbral
                        st.success(f"✅ Acceso concedido. Imagen similar encontrada: {archivo}")
                        match_found = True
                        break
            if not match_found:
                st.error("❌ Acceso denegado. Rostro no reconocido (comparación básica).")

        # Resetear cámara después de capturar
        st.session_state.show_validation_camera = False