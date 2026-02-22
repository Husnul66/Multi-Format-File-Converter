# ♻️ Süper Dönüştürücü (Multi-Format File Converter)

Bu proje, Python ve Streamlit kullanılarak geliştirilmiş, tamamen bulut üzerinde 7/24 çalışan çok amaçlı bir dosya dönüştürme web uygulamasıdır (Web App). Kullanıcıların bilgisayarlarına herhangi bir yazılım kurmasına gerek kalmadan, doğrudan tarayıcı üzerinden dosya formatlarını dönüştürmesini sağlar.

### 🚀 [UYGULAMAYI CANLI KULLANMAK İÇİN BURAYA TIKLAYIN]([BURAYA_LINK_GELECEK](https://formatconverter.streamlit.app/))

## ✨ Özellikler ve Yetenekler

Uygulama akıllı bir kullanıcı arayüzüne (UI) sahiptir. Kullanıcının yüklediği dosya formatını analiz eder ve yalnızca mantıksal olarak dönüştürülebilecek hedef format seçeneklerini dinamik olarak gösterir.

- **Belge Dönüşümleri:** Word, Excel ve PowerPoint dosyalarını yüksek sadakatle PDF formatına çevirme.
- **Tersine ve Zincirleme Dönüşümler:** PDF dosyalarını düzenlenebilir Word formatına dönüştürme. PowerPoint sunumlarını doğrudan Word belgesi haline getirme.
- **Medya İşleme:** Video dosyalarından (örn. MP4) ses ayrıştırma (MP3) ve format dönüştürme işlemleri.
- **Görsel Dönüşümleri:** Farklı resim formatları arasında dönüşüm yapma ve görselleri PDF'e derleme.

## 🛠️ Kullanılan Teknolojiler (Tech Stack)

- **Frontend & Deployment:** `Streamlit` (Community Cloud üzerinden Serverless Deployment)
- **Belge İşleme:** `pdf2docx`, `python-docx`
- **Medya İşleme (Video/Ses):** `moviepy` (Arka planda FFmpeg altyapısı ile)
- **Görsel İşleme:** `Pillow` (PIL)
- **Sistem Kütüphaneleri:** `packages.txt` üzerinden Linux Debian paket yönetimi.

## 💻 Geliştiriciler İçin Yerel Kurulum (Local Development)

Projeyi bilgisayarınızda (Localhost) çalıştırmak ve geliştirmek isterseniz aşağıdaki adımları izleyebilirsiniz:

1. Depoyu bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/KULLANICI_ADIN/Husnu_Donusturucu.git](https://github.com/KULLANICI_ADIN/Husnu_Donusturucu.git)
   cd Husnu_Donusturucu
