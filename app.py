import streamlit as st
import os
import subprocess
import shutil
from PIL import Image

# --- STREAMLIT CLOUD (LINUX) UYUMLU SÜRÜM ---

st.set_page_config(page_title="Husnu Super Dönüştürücü", page_icon="⚡", layout="centered")

# Geçici klasör ayarları
def setup_folders():
    if os.path.exists("temp"): shutil.rmtree("temp")
    if os.path.exists("output"): shutil.rmtree("output")
    os.makedirs("temp")
    os.makedirs("output")

# LibreOffice kontrolü
def get_libreoffice_command():
    if shutil.which("libreoffice"):
        return "libreoffice"
    elif shutil.which("soffice"):
        return "soffice"
    return None

def convert_document(input_path, cmd_name):
    cmd = [cmd_name, '--headless', '--convert-to', 'pdf', '--outdir', 'output', input_path]
    subprocess.run(cmd, check=True)
    filename = os.path.basename(input_path)
    name_only = os.path.splitext(filename)[0]
    return os.path.join("output", f"{name_only}.pdf")

def convert_media_ffmpeg(input_path, target_ext):
    filename = os.path.basename(input_path)
    name_only = os.path.splitext(filename)[0]
    output_path = os.path.join("output", f"{name_only}.{target_ext}")
    
    cmd = ['ffmpeg', '-i', input_path]
    if target_ext in ['mp3', 'wav', 'flac']:
         cmd.extend(['-vn', '-acodec', 'libmp3lame', '-q:a', '2']) if target_ext == 'mp3' else cmd.extend(['-vn'])
    cmd.append(output_path)
    cmd.append('-y')

    subprocess.run(cmd, check=True)
    return output_path

def convert_image(input_path, target_ext):
    filename = os.path.basename(input_path)
    name_only = os.path.splitext(filename)[0]
    output_path = os.path.join("output", f"{name_only}.{target_ext}")
    img = Image.open(input_path)
    if target_ext in ['jpg', 'pdf'] and img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save(output_path, target_ext.upper() if target_ext != 'jpg' else 'JPEG')
    return output_path

# --- ARAYÜZ ---
st.title("⚡ Online Dönüştürücü")
st.caption("Streamlit Cloud üzerinde çalışıyor")

# setup_done kontrolü ile klasörleri sadece bir kez sıfırla
if 'setup_done' not in st.session_state:
    setup_folders()
    st.session_state['setup_done'] = True

uploaded_file = st.file_uploader("Dosya Yükle", type=['docx','xlsx','pptx','pdf','png','jpg','mp4','mp3','wav'])

if uploaded_file:
    # Dosyayı kaydet
    temp_path = os.path.join("temp", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    target = st.selectbox("Format Seç", ['pdf', 'mp3', 'wav', 'png', 'jpg'])
    
    if st.button("Çevir"):
        try:
            out_file = None
            with st.spinner('Dönüştürülüyor...'): # Kullanıcıya işlem olduğunu gösterir
                if target == 'pdf' and ext in ['.docx','.xlsx','.pptx']:
                    lo_cmd = get_libreoffice_command()
                    if lo_cmd:
                        out_file = convert_document(temp_path, lo_cmd)
                    else:
                        st.error("Sunucuda LibreOffice bulunamadı. packages.txt dosyasını kontrol et.")
                elif target in ['mp3','wav'] and ext in ['.mp4','.m4a','.wav','.mp3']:
                    out_file = convert_media_ffmpeg(temp_path, target)
                elif target in ['
