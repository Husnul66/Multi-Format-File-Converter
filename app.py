import streamlit as st
import os
import subprocess
import shutil
from PIL import Image
from pdf2docx import Converter

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

def convert_pdf_to_word(input_path):
    filename = os.path.basename(input_path)
    name_only = os.path.splitext(filename)[0]
    output_path = os.path.join("output", f"{name_only}.docx")
    cv = Converter(input_path)
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

# --- ARAYÜZ VE MANTIK ---
st.title("⚡ Super Dönüştürücü")
st.caption("PDF ↔ Word | Video ➡️ Ses | Resim Çevirici")

if 'setup_done' not in st.session_state:
    setup_folders()
    st.session_state['setup_done'] = True

uploaded_file = st.file_uploader("Dosya Yükle", type=['docx','xlsx','pptx','ppt','pdf','png','jpg','jpeg','mp4','mp3','wav','m4a'])

if uploaded_file:
    # Dosyayı kaydet
    temp_path = os.path.join("temp", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    # --- AKILLI SEÇENEK SİSTEMİ BURADA ---
    # Hangi dosya yüklendiğinde hangi seçenekler çıkacak?
    conversion_map = {
        '.docx': ['pdf'],
        '.xlsx': ['pdf'],
        '.pptx': ['pdf', 'docx'], # PPT hem PDF hem Word olabilir
        '.ppt':  ['pdf', 'docx'],
        '.pdf':  ['docx'],
        '.mp4':  ['mp3', 'wav'],
        '.m4a':  ['mp3', 'wav'],
        '.mp3':  ['wav'],
        '.wav':  ['mp3'],
        '.png':  ['jpg', 'pdf'],
        '.jpg':  ['png', 'pdf'],
        '.jpeg': ['png', 'pdf']
    }

    # Dosya uzantısına göre listeyi getir, eğer yoksa boş liste ver
    valid_options = conversion_map.get(ext, [])

    if not valid_options:
        st.error(f"Bu dosya formatı ({ext}) için tanımlı bir dönüşüm yok.")
    else:
        # Selectbox artık sadece 'valid_options' listesini gösteriyor
        target = st.selectbox(f"Hedef Formatı Seç ({ext} dosyanız için):", valid_options)
        
        if st.button("Çevir"):
            try:
                out_file = None
                with st.spinner('İşleniyor...'):
                    
                    # 1. KURAL: Ofis -> PDF
                    if target == 'pdf' and ext in ['.docx','.xlsx','.pptx','.ppt']:
                        lo_cmd = get_libreoffice_command()
                        if lo_cmd: out_file = convert_document(temp_path, lo_cmd)
                        else: st.error("LibreOffice bulunamadı.")
                    
                    # 2. KURAL: PDF -> Word
                    elif target == 'docx' and ext == '.pdf':
                        out_file = convert_pdf_to_word(temp_path)

                    # 3. KURAL: PowerPoint -> Word (Zincirleme)
                    elif target == 'docx' and ext in ['.pptx', '.ppt']:
                        st.info("En iyi sonuç için önce PDF'e, sonra Word'e dönüştürülüyor...")
                        lo_cmd = get_libreoffice_command()
                        if lo_cmd:
                            temp_pdf = convert_document(temp_path, lo_cmd)
                            out_file = convert_pdf_to_word(temp_pdf)
                        else: st.error("LibreOffice bulunamadı.")

                    # 4. KURAL: Medya -> Ses
                    elif target in ['mp3','wav'] and ext in ['.mp4','.m4a','.wav','.mp3']:
                        out_file = convert_media_ffmpeg(temp_path, target)
                    
                    # 5. KURAL: Resim -> Resim/PDF
                    elif target in ['png','jpg','pdf']:
                        out_file = convert_image(temp_path, target)

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

