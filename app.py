import streamlit as st
import yt_dlp
import whisper
import os
import tempfile
import shutil
import subprocess

# FFmpeg ve ffprobe kontrolü
def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(["ffprobe", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, "FFmpeg ve ffprobe yüklü."
    except Exception as e:
        return False, f"FFmpeg veya ffprobe eksik: {e}"

def download_audio(url, temp_dir):
    output_path = os.path.join(temp_dir, "audio.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # Dosya adını bul
        if 'requested_downloads' in info:
            filename = info['requested_downloads'][0]['filepath']
        elif 'url' in info:
            filename = ydl.prepare_filename(info)
            filename = os.path.splitext(filename)[0] + '.mp3'
        else:
            filename = os.path.join(temp_dir, "audio.mp3")
        return filename

def transcribe_audio(audio_path, model_name, language):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language=language)
    return result['text']

# Modern ve kullanıcı dostu arayüz
st.set_page_config(page_title="YouTube Transkript", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f7f7fa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stTextInput>div>div>input {
        font-size: 1.1rem;
    }
    .stTextArea textarea {
        font-size: 1.05rem;
        background: #f4f4f4;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4f8cff 0%, #235390 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-size: 1.1rem;
    }
    .stDownloadButton>button {
        background: #e0e7ff;
        color: #1e293b;
        font-weight: 600;
        border-radius: 8px;
        font-size: 1rem;
    }
    .stAlert {
        font-size: 1.05rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
# 🎤 YEREL ETKİLEŞİM BİRİMİ 🎤
# 🎤 YouTube Video Transkript Oluşturucu 🎤
YouTube video URL'sini girin, dili ve modeli seçin, transkripti saniyeler içinde alın!  
<sub>Powered by OpenAI Whisper & yt-dlp</sub>
---
""", unsafe_allow_html=True)

with st.container():
    st.subheader("🔗 Video Bilgileri")
    video_url = st.text_input("YouTube Video URL'si", placeholder="https://www.youtube.com/watch?v=VIDEO_ID")
    language = st.selectbox("Transkript Dili", ["Türkçe (tr)", "İngilizce (en)", "Almanca (de)", "Fransızca (fr)", "İspanyolca (es)"])
    language_code = language.split("(")[-1].replace(")", "").strip()
    model_name = st.selectbox("Whisper Modeli (Hız vs Doğruluk)", ["tiny", "base", "small", "medium", "large"])

ffmpeg_ok, ffmpeg_msg = check_ffmpeg()
if not ffmpeg_ok:
    st.error(ffmpeg_msg)
    st.stop()

temp_dir = tempfile.mkdtemp()
audio_file = os.path.join(temp_dir, "audio.mp3")

with st.container():
    st.subheader("📝 Transkript İşlemi")
    if st.button("🚀 Transkript Oluştur", use_container_width=True):
        if not video_url:
            st.error("Lütfen bir YouTube URL'si girin!")
        else:
            with st.spinner("🎵 Video sesi indiriliyor..."):
                try:
                    audio_path = download_audio(video_url, temp_dir)
                    if not os.path.exists(audio_path):
                        st.error(f"Ses dosyası oluşturulmadı: {audio_path}")
                        shutil.rmtree(temp_dir, ignore_errors=True)
                        st.stop()
                    else:
                        st.success("Ses dosyası başarıyla indirildi!")
                except Exception as e:
                    st.error(f"Ses indirme hatası: {str(e)}")
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    st.stop()

            with st.spinner("🧠 Transkript oluşturuluyor..."):
                try:
                    transcript = transcribe_audio(audio_path, model_name, language_code)
                    st.success("Transkript hazır!")
                    st.text_area("Transkript", transcript, height=300, key="transcript_area")
                    st.download_button(
                        label="⬇️ Transkripti İndir",
                        data=transcript,
                        file_name="transkript.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"Transkripsiyon hatası: {str(e)}")
                finally:
                    shutil.rmtree(temp_dir, ignore_errors=True)

st.markdown("""
---
<div style='text-align:center; color: #888;'>
2025 © Lokal YouTube Transkript Oluşturucu
</div>
""", unsafe_allow_html=True)