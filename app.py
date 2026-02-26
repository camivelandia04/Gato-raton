import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ---------------- CONFIGURACIÓN ----------------
MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB en bytes

st.title("🎧 Asistente de lectura para estudiantes")

# Imagen (SE MANTIENE)
image = Image.open('jovenescuchando.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("✍️ Escribe y/o selecciona texto para ser escuchado.")

# Crear carpeta temporal
if not os.path.exists("temp"):
    os.mkdir("temp")

# Texto informativo (SE MANTIENE)
st.subheader("📚 ¿De qué trata?")
st.write(
    '¡Aqui puedes poner tus textos o articulos académicos y yo los pasaré a audio '
    'para que puedas esuccharlos mientras vas al trabajo, a la u o mientras haces otras actividades'
)

st.markdown("🔊 **¿Quieres escucharlo? Copia el texto o sube un archivo**")

# -------- NUEVO: subir archivo TXT ----------
uploaded_file = st.file_uploader(
    "📄 Subir archivo .txt (máximo 1GB)",
    type=["txt"]
)

text = ""

if uploaded_file is not None:
    if uploaded_file.size > MAX_FILE_SIZE:
        st.error("🚫 El archivo supera el tamaño máximo permitido (1 GB).")
    else:
        text = uploaded_file.read().decode("utf-8")
        st.success("✅ Archivo cargado correctamente")

# Área de texto manual
text_input = st.text_area("📝 O ingrese el texto a escuchar:")
if text_input:
    text = text_input

# -------- Información del texto ----------
if text:
    palabras = len(text.split())
    tiempo_estimado = round(palabras / 150, 1)
    st.info(f"📊 {palabras} palabras | ⏱ Tiempo estimado: {tiempo_estimado} min")

# Idioma
option_lang = st.selectbox(
    "🌎 Selecciona el lenguaje",
    ("Español", "English")
)

lg = "es" if option_lang == "Español" else "en"

# Título del audio
titulo_audio = st.text_input("🎙️ Título del audio (opcional)")

# -------- Función TTS ----------
def text_to_speech(text, lg, titulo):
    tts = gTTS(text, lang=lg)

    if titulo:
        my_file_name = titulo.replace(" ", "_")
    else:
        my_file_name = "audio_estudio"

    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name


# -------- BOTÓN PRINCIPAL ----------
if st.button("🎧 Convertir a Audio"):

    if text.strip() == "":
        st.warning("⚠️ Debes ingresar texto primero.")
    else:
        result = text_to_speech(text, lg, titulo_audio)

        with open(f"temp/{result}.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.success("✅ Audio generado correctamente")
        st.markdown("## 🔊 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3")

        # Descargar audio
        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">⬇ Descargar {file_label}</a>'
            return href

        st.markdown(
            get_binary_file_downloader_html(f"{result}.mp3", "Audio"),
            unsafe_allow_html=True
        )

# -------- Limpieza automática ----------
def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
