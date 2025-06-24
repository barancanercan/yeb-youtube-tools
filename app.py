import streamlit as st
import yt_dlp
import whisper
import os
import tempfile
import shutil
import subprocess
import google.generativeai as genai
from datetime import datetime

# .env dosyasını manuel olarak oku
def load_env_file():
    """Manuel olarak .env dosyasını oku"""
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except FileNotFoundError:
        pass

# Gemini API yapılandırması
def configure_gemini():
    """Gemini API'yi yapılandır"""
    # Önce .env dosyasını yükle
    load_env_file()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')
    except Exception:
        return None

def create_summary_prompt(transcript, video_title=""):
    """Profesyonel özet için prompt oluştur"""
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    prompt = f"""
Aşağıdaki YouTube video transkriptini profesyonel bir şekilde özetleyiniz.

VIDEO BİLGİLERİ:
- Başlık: {video_title if video_title else "Belirtilmemiş"}
- Özet Tarihi: {current_date}

TRANSKRİPT:
{transcript}

ÖZET REHBERİ:
Lütfen aşağıdaki formatta detaylı bir özet hazırlayın:

## 📋 GENEL ÖZET
Video içeriğinin ana konusunu ve amacını 2-3 cümlede özetleyin.

## 🎯 ANA KONULAR
- Videoda ele alınan temel konuları madde halinde listeleyin
- Her konu için kısa açıklama ekleyin

## 🔍 ANAHTAR NOKTALAR
Videodaki en önemli bilgi, iddia veya argümanları vurgulayın:
- Önemli veriler, istatistikler
- Dikkat çekici iddialar
- Uzman görüşleri
- Sonuçlar ve öneriler

## 🗞️ GÜNDEM İLE İLİŞKİSİ
Eğer video içeriği güncel olaylar, siyaset, ekonomi, teknoloji, sosyal konular gibi gündemle ilgili konulara değiniyorsa:
- Hangi güncel konularla bağlantılı olduğunu belirtin
- Türkiye ve dünya gündemine etkisini değerlendirin

## 💡 ÖNE ÇIKAN ALINTILAR
Videodaki en etkileyici veya önemli alıntıları (varsa) ekleyin.

## 📊 HEDEF KİTLE VE UYGULANMA
- Bu bilgi kimler için faydalı?
- Pratik uygulamaları neler?

ÖNEMLI NOTLAR:
- Objektif ve tarafsız kalın
- Türkçe dilbilgisi kurallarına uyun
- Profesyonel ve anlaşılır bir dil kullanın
- Transkriptte geçmeyen bilgi eklemeyin
"""
    return prompt

def analyze_transcript_with_gemini(model, transcript, video_title=""):
    """Gemini ile transkript analizi ve özetleme"""
    try:
        prompt = create_summary_prompt(transcript, video_title)
        
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 4000,
            }
        )
        
        return response.text if response.text else "Özet oluşturulamadı."
            
    except Exception as e:
        return f"Gemini API hatası: {str(e)}"

def get_video_info(url):
    """Video başlığı ve meta bilgileri al"""
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', ''),
            }
    except Exception:
        return {}

def check_ffmpeg():
    """FFmpeg kontrolü"""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, "FFmpeg yüklü."
    except Exception as e:
        return False, f"FFmpeg eksik: {e}"

def download_audio(url, temp_dir):
    """Video sesini indir"""
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
        if 'requested_downloads' in info:
            return info['requested_downloads'][0]['filepath']
        else:
            return os.path.join(temp_dir, "audio.mp3")

def transcribe_audio(audio_path, model_name, language):
    """Ses dosyasını metne çevir"""
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path, language=language)
    return result['text']

# Streamlit sayfa ayarları
st.set_page_config(
    page_title="YEB AI YouTube Özetleyici",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Siyah tema CSS
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    .block-container {
        max-width: 1000px;
        padding-left: 2rem;
        padding-right: 2rem;
        margin: 0 auto;
    }
    
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .content-container {
        background-color: #1e2329;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #333;
        margin: 1rem 0;
    }
    
    .result-container {
        background-color: #2d3748;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #2d3748;
        color: #fafafa;
        border: 1px solid #4a5568;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > select {
        background-color: #2d3748;
        color: #fafafa;
        border: 1px solid #4a5568;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #2d3748;
        color: #fafafa;
        border: 1px solid #4a5568;
        border-radius: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stDownloadButton > button {
        background-color: #4a5568;
        color: #fafafa;
        border: 1px solid #667eea;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        width: 100%;
    }
    
    .info-card {
        background-color: #2d3748;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4a5568;
        margin: 0.5rem 0;
    }
    
    .warning-card {
        background-color: #744210;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #f6ad55;
        margin: 1rem 0;
    }
    
    .success-card {
        background-color: #276749;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #68d391;
        margin: 1rem 0;
    }
    
    .status-text {
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">🎬 YEB AI YouTube Özetleyici</h1>', unsafe_allow_html=True)

# Gemini model kontrolü
gemini_model = configure_gemini()

# FFmpeg kontrolü
ffmpeg_ok, ffmpeg_msg = check_ffmpeg()
if not ffmpeg_ok:
    st.error(f"❌ {ffmpeg_msg}")
    st.stop()

# Ana içerik
st.markdown('<div class="content-container">', unsafe_allow_html=True)

# Video URL girişi
video_url = st.text_input(
    "📺 YouTube Video URL'si",
    placeholder="https://www.youtube.com/watch?v=VIDEO_ID",
    help="YouTube video linkini buraya yapıştırın"
)

# Ayarlar
col1, col2, col3 = st.columns(3)

with col1:
    language = st.selectbox(
        "🌍 Dil",
        ["Türkçe (tr)", "İngilizce (en)", "Almanca (de)", "Fransızca (fr)", "İspanyolca (es)"]
    )
    language_code = language.split("(")[-1].replace(")", "").strip()

with col2:
    model_name = st.selectbox(
        "🧠 Model",
        ["tiny", "base", "small", "medium", "large"],
        index=1,
        help="Tiny: Hızlı, Large: Daha doğru"
    )

with col3:
    create_summary = st.checkbox(
        "🤖 AI Özet",
        value=bool(gemini_model),
        disabled=not bool(gemini_model),
        help="Gemini ile akıllı özet oluştur"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Video bilgilerini göster
if video_url:
    with st.spinner("📹 Video bilgileri alınıyor..."):
        video_info = get_video_info(video_url)
        if video_info and video_info.get('title'):
            st.markdown(f"""
            <div class="info-card">
                <strong>📺 {video_info['title']}</strong><br>
                <span class="status-text">👤 {video_info.get('uploader', 'Bilinmiyor')}</span>
                {f"<span class='status-text'>⏱️ {video_info['duration']//60}:{video_info['duration']%60:02d}</span>" if video_info.get('duration') else ""}
            </div>
            """, unsafe_allow_html=True)

# Ana işlem butonu
if st.button("🚀 Analizi Başlat", type="primary"):
    if not video_url:
        st.error("❌ Lütfen bir YouTube URL'si girin!")
    else:
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 1. Ses indirme
            with st.spinner("🎵 Video sesi indiriliyor..."):
                audio_path = download_audio(video_url, temp_dir)
                if not os.path.exists(audio_path):
                    st.error("❌ Ses dosyası oluşturulamadı!")
                    st.stop()
            
            st.markdown('<div class="success-card">✅ Ses dosyası hazır!</div>', unsafe_allow_html=True)

            # 2. Transkripsiyon
            with st.spinner("🧠 Konuşma metne dönüştürülüyor..."):
                transcript = transcribe_audio(audio_path, model_name, language_code)
            
            st.markdown('<div class="success-card">✅ Transkript oluşturuldu!</div>', unsafe_allow_html=True)

            # 3. Sonuçları göster
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📝 Ham Transkript")
                st.text_area(
                    "transcript_content",
                    transcript,
                    height=400,
                    label_visibility="collapsed"
                )
                st.download_button(
                    "📥 Transkripti İndir",
                    data=transcript,
                    file_name=f"transkript_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )

            with col2:
                if create_summary and gemini_model:
                    st.markdown("### 🤖 AI Özetleme")
                    with st.spinner("🔮 AI özet hazırlanıyor..."):
                        video_title = video_info.get('title', '') if video_info else ''
                        summary = analyze_transcript_with_gemini(gemini_model, transcript, video_title)
                    
                    st.markdown(f'<div class="result-container">{summary}</div>', unsafe_allow_html=True)
                    
                    st.download_button(
                        "📥 AI Özetini İndir",
                        data=summary,
                        file_name=f"ai_ozet_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.markdown("### ℹ️ Bilgi")
                    st.info("AI özet özelliği için Gemini API anahtarı gerekli.")

        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

# Alt bilgi
st.markdown("""
---
<div style='text-align:center; color: #718096; font-size: 0.9rem; padding: 2rem 0;'>
    🤖 <strong>Powered by</strong> OpenAI Whisper • Google Gemini 1.5 Flash<br>
    <em>Profesyonel Video Analizi Sistemi</em>
    <em>Created by Baran Can Ercan</em>
</div>
""", unsafe_allow_html=True)