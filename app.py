import streamlit as st
import os
import subprocess
import shutil
from PIL import Image
from pdf2docx import Converter # <--- YENİ KÜTÜPHANE EKLENDİ

# --- STREAMLIT AYARLARI ---
st.set_page_config(page_title="Husnu Super Dönüştürücü", page_icon="⚡", layout="centered")

def setup_folders():
    if os.path.exists("temp"): shutil.rmtree("temp")
    if os.path.exists("output"): shutil.rmtree("output")
    os.makedirs("temp")
    os.makedirs("output")

def get_libreoffice_command():
    if shutil.which("libreoffice"): return "libreoffice"
    elif shutil.which("soffice"): return "soffice"
    return None

# --- DÖNÜŞTÜRME FONKSİYONLARI ---

def convert_document(input_path, cmd_name):
    # Word/Excel -> PDF
    cmd = [cmd_name, '--headless', '--convert-to', 'pdf', '--outdir', 'output', input_path]
    subprocess.run(cmd, check=True)
    filename = os.path.basename(input_path)
    name_only = os.path.splitext(filename)[0]
    return os.path.join("output", f"{name_only}.pdf")

# [YENİ FONKSİYON] PDF -> Word
def convert_pdf_to_word(input_path):
    filename = os.path.basename(input_path)
    name_only = os.path.splitext(filename)[0]
    output_path = os.path.join("output", f"{name_only}.docx")
    
    cv = Converter(input_path)
    # start=0, end=None (Tüm sayfaları dönüştür)
    cv.convert(output_path, start=0, end=None)
    cv.close()
    return output_path

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
st.title("⚡ Husnu Super Dönüştürücü")
st.caption("PDF ↔ Word | Video ➡️ Ses | Resim Çevirici")

if 'setup_done' not in st.session_state:
    setup_folders()
    st.session_state['setup_done'] = True

# PDF dosya türünü de yüklemeye izin veriyoruz
uploaded_file = st.file_uploader("Dosya Yükle", type=['docx','xlsx','pptx','pdf','png','jpg','mp4','mp3','wav'])

if uploaded_file:
    temp_path = os.path.join("temp", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    
    # Hedef format listesine 'docx' ekledik
    target = st.selectbox("Format Seç", ['pdf', 'docx', 'mp3', 'wav', 'png', 'jpg'])
    
    if st.button("Çevir"):
        try:
            out_file = None
            with st.spinner('İşleniyor...'):
                
                # 1. Durum: Ofis -> PDF
                if target == 'pdf' and ext in ['.docx','.xlsx','.pptx']:
                    lo_cmd = get_libreoffice_command()
                    if lo_cmd: out_file = convert_document(temp_path, lo_cmd)
                    else: st.error("LibreOffice bulunamadı.")
                
                # 2. Durum: PDF -> Word (YENİ EKLENEN KISIM)
                elif target == 'docx' and ext == '.pdf':
                    out_file = convert_pdf_to_word(temp_path)

                # 3. Durum: Medya -> Ses
                elif target in ['mp3','wav'] and ext in ['.mp4','.m4a','.wav','.mp3']:
                    out_file = convert_media_ffmpeg(temp_path, target)
                
                # 4. Durum: Resim -> Resim/PDF
                elif target in ['png','jpg','pdf']:
                    out_file = convert_image(temp_path, target)
                
                else:
                    st.warning(f"{ext} formatından {target} formatına dönüşüm desteklenmiyor.")

            if out_file and os.path.exists(out_file):
                st.success("İşlem Başarılı!")
                with open(out_file, "rb") as f:
                    file_data = f.read()
                st.download_button(
                    label="İndir", 
                    data=file_data, 
                    file_name=os.path.basename(out_file),
                    mime="application/octet-stream"
                )
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
