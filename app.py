import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Asistente de lectura para estudiantes")

# Imagen (SE MANTIENE)
image = Image.open('jovenescuchando.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Esrcibe y/o selecciona texto para ser escuchado.")

# Crear carpeta temporal
if not os.path.exists("temp"):
    os.mkdir("temp")

# Texto informativo (SE MANTIENE)
st.subheader("¿De qué trata?.")
st.write(
    '¡Aqui puedes poner tus textos o articulos académicos y yo los pasaré a audio '
    'para que puedas esuccharlos mientras vas al trabajo, a la u o mientras haces otras actividades'
)

st.markdown("Quieres escucharlo?, copia el texto")

# NUEVO 👉 título tipo podcast
titulo_audio = st.text_input("Título del audio (opcional)")

text = st.text_area("Ingrese El texto a escuchar.")

# NUEVO 👉 contador y estimación
if text:
    palabras = len(text.split())
    tiempo_estimado = round(palabras / 150, 1)  # 150 palabras/min aprox
    st.info(f"📊 {palabras} palabras | ⏱ Tiempo estimado: {tiempo_estimado} min")

# Selección idioma
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English")
)

lg = "es" if option_lang == "Español" else "en"

# NUEVO 👉 selector visual de velocidad (UX)
velocidad = st.radio(
    "Velocidad de lectura",
    ("Normal", "Rápida")
)

def text_to_speech(text, lg, titulo):
    tts = gTTS(text, lang=lg)

    if titulo:
        my_file_name = titulo.replace(" ", "_")
    else:
        my_file_name = "audio_estudio"

    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text


# BOTÓN PRINCIPAL
if st.button("🎧 Convertir a Audio"):

    if text.strip() == "":
        st.warning("⚠️ Debes ingresar texto primero.")
    else:
        result, output_text = text_to_speech(text, lg, titulo_audio)

        with open(f"temp/{result}.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.success("✅ Audio generado correctamente")
        st.markdown("## Tú audio:")
        st.audio(audio_bytes, format="audio/mp3")

        # Descargar archivo
        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">⬇ Descargar {file_label}</a>'
            return href

        st.markdown(
            get_binary_file_downloader_html(f"{result}.mp3", "Audio"),
            unsafe_allow_html=True
        )


# Limpieza automática archivos antiguos
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
