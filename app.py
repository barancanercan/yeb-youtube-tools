import streamlit as st
import yt_dlp
import whisper
import os
import tempfile
import shutil
import subprocess
import google.generativeai as genai
from datetime import datetime
import concurrent.futures
from pydub import AudioSegment
import threading
import time

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
@st.cache_resource
def configure_gemini():
    """Gemini API'yi yapılandır - Cache'lenir"""
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

# Whisper modelini cache'le
@st.cache_resource
def load_whisper_model(model_name):
    """Whisper modelini yükle ve cache'le"""
    return whisper.load_model(model_name)

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

@st.cache_data
def get_video_info(url):
    """Video başlığı ve meta bilgileri al - Cache'lenir"""
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

@st.cache_resource
def check_ffmpeg():
    """FFmpeg kontrolü - Cache'lenir"""
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True, "FFmpeg yüklü."
    except Exception as e:
        return False, f"FFmpeg eksik: {e}"

def download_audio(url, temp_dir):
    """Video sesini indir - Optimize edildi"""
    output_path = os.path.join(temp_dir, "audio.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio[filesize<50M]/bestaudio/best[filesize<50M]',  # Dosya boyutu sınırı
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extractaudio': True,
        'audioformat': 'mp3',
        'audioquality': '5',  # Daha düşük kalite, daha hızlı
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',  # Düşük kalite
        }],
        # Hız optimizasyonları
        'extractor_retries': 1,
        'fragment_retries': 1,
        'retries': 1,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'requested_downloads' in info:
                return info['requested_downloads'][0]['filepath']
            else:
                return os.path.join(temp_dir, "audio.mp3")
    except Exception as e:
        # Fallback: en düşük kalite
        ydl_opts['format'] = 'worst'
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if 'requested_downloads' in info:
                return info['requested_downloads'][0]['filepath']
            else:
                return os.path.join(temp_dir, "audio.mp3")

def split_audio_into_chunks(audio_path, chunk_length_ms=60000):
    """Ses dosyasını parçalara böl - varsayılan 1 dakika"""
    try:
        audio = AudioSegment.from_file(audio_path)
        chunks = []
        
        # Ses dosyası kısa ise bölmeye gerek yok
        if len(audio) <= chunk_length_ms:
            return [audio_path]
        
        temp_dir = os.path.dirname(audio_path)
        chunk_paths = []
        
        for i, chunk_start in enumerate(range(0, len(audio), chunk_length_ms)):
            chunk_end = min(chunk_start + chunk_length_ms, len(audio))
            chunk = audio[chunk_start:chunk_end]
            
            chunk_path = os.path.join(temp_dir, f"chunk_{i:03d}.mp3")
            chunk.export(chunk_path, format="mp3")
            chunk_paths.append((chunk_path, chunk_start / 1000))  # saniye cinsinden başlangıç zamanı
            
        return chunk_paths
    except Exception as e:
        st.warning(f"Ses dosyası bölünemiyor, tek parça işlenecek: {e}")
        return [audio_path]

def transcribe_chunk(chunk_info, model_name, language):
    """Tek bir ses parçasını metne çevir - Thread-safe"""
    chunk_path, start_time = chunk_info
    try:
        # Her thread kendi modelini yükler (thread-safe)
        import whisper
        model = whisper.load_model(model_name)
        
        result = model.transcribe(
            chunk_path,
            language=language,
            fp16=False,
            verbose=False,
            beam_size=1,
            best_of=1,
        )
        # Model'i memory'den temizle
        del model
        return (start_time, result['text'])
    except Exception as e:
        return (start_time, f"[Hata: {str(e)}]")

def transcribe_audio_parallel(audio_path, model_name, language, chunk_length_minutes=1):
    """Ses dosyasını paralel olarak metne çevir - İyileştirilmiş versiyon"""
    chunk_length_ms = chunk_length_minutes * 60 * 1000
    
    # Progress container oluştur
    progress_container = st.empty()
    status_container = st.empty()
    
    # Ses dosyasını parçalara böl
    with progress_container:
        progress_bar = st.progress(0, text="🔪 Ses dosyası parçalanıyor...")
    
    chunk_paths = split_audio_into_chunks(audio_path, chunk_length_ms)
    
    if isinstance(chunk_paths[0], str):  # Tek dosya
        with progress_container:
            progress_bar = st.progress(50, text="📝 Transkripsiyon yapılıyor...")
        
        import whisper
        model = whisper.load_model(model_name)
        result = model.transcribe(
            audio_path,
            language=language,
            fp16=False,
            verbose=False,
            beam_size=1,
            best_of=1,
        )
        
        with progress_container:
            progress_bar = st.progress(100, text="✅ Tamamlandı!")
        
        progress_container.empty()
        return result['text']
    
    # Paralel işleme için optimum thread sayısı
    max_workers = min(3, len(chunk_paths), os.cpu_count() or 1)
    
    with status_container:
        st.info(f"🚀 {len(chunk_paths)} parça, {max_workers} thread ile işleniyor...")
    
    with progress_container:
        progress_bar = st.progress(25, text=f"🚀 Paralel işleme başlatılıyor...")
    
    transcriptions = []
    completed_chunks = []
    
    # Process tracking için
    import queue
    result_queue = queue.Queue()
    
    def worker_with_queue(chunk_info):
        """Worker function that puts results in queue"""
        result = transcribe_chunk(chunk_info, model_name, language)
        result_queue.put(result)
        return result
    
    # ThreadPoolExecutor ile paralel işleme
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # İşleri başlat
        futures = []
        for chunk_info in chunk_paths:
            future = executor.submit(worker_with_queue, chunk_info)
            futures.append(future)
        
        # Sonuçları topla
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                start_time, text = future.result()
                transcriptions.append((start_time, text))
                completed += 1
                
                # Progress güncelle
                progress = 25 + (completed / len(chunk_paths)) * 65
                with progress_container:
                    progress_bar = st.progress(
                        int(progress), 
                        text=f"📝 {completed}/{len(chunk_paths)} parça tamamlandı..."
                    )
                
            except Exception as e:
                completed += 1
                transcriptions.append((0, f"[İşleme hatası: {str(e)}]"))
                with progress_container:
                    progress_bar = st.progress(
                        int(25 + (completed / len(chunk_paths)) * 65), 
                        text=f"⚠️ {completed}/{len(chunk_paths)} parça işlendi (bazı hatalar var)..."
                    )
    
    # Parçaları zamana göre sırala ve birleştir
    with progress_container:
        progress_bar = st.progress(95, text="🔗 Parçalar birleştiriliyor...")
    
    transcriptions.sort(key=lambda x: x[0])  # Zamana göre sırala
    
    # Metinleri birleştir
    full_transcript = " ".join([text.strip() for _, text in transcriptions if text.strip()])
    
    # Geçici chunk dosyalarını temizle
    for chunk_path, _ in chunk_paths:
        try:
            if os.path.exists(chunk_path):
                os.remove(chunk_path)
        except:
            pass
    
    with progress_container:
        progress_bar = st.progress(100, text="✅ Transkripsiyon tamamlandı!")
    
    # Containers'ı temizle
    time.sleep(1)
    progress_container.empty()
    status_container.empty()
    
    return full_transcript

# Streamlit sayfa ayarları
st.set_page_config(
    page_title="YEB AI YouTube Özetleyici",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Session state başlatma
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = ""
if 'video_info' not in st.session_state:
    st.session_state.video_info = {}

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
        margin: 0.25rem 0;
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
    
    .stRadio > div {
        background-color: #2d3748;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4a5568;
    }
    
    .option-container {
        background-color: #1a202c;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #4a5568;
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

# Ayarlar bölümü
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "🌍 Dil",
        ["Türkçe (tr)", "İngilizce (en)", "Almanca (de)", "Fransızca (fr)", "İspanyolca (es)"]
    )
    language_code = language.split("(")[-1].replace(")", "").strip()

with col2:
    model_name = st.selectbox(
        "🧠 Whisper Model",
        ["tiny", "base", "small", "medium", "large"],
        index=1,
        help="Tiny: En hızlı | Base: Önerilen | Large: En doğru"
    )

# Paralel işleme ayarları
st.markdown('<div class="option-container">', unsafe_allow_html=True)
st.markdown("### ⚡ Hız Optimizasyonu")

col3, col4 = st.columns(2)
with col3:
    chunk_length = st.selectbox(
        "🔪 Parça Uzunluğu (dakika)",
        [0.5, 1, 2, 3, 5],
        index=1,
        help="Kısa parçalar = Daha hızlı paralel işleme"
    )

with col4:
    use_parallel = st.checkbox(
        "🚀 Paralel İşleme",
        value=True,
        help="Ses dosyasını parçalara bölüp paralel işler (Çok daha hızlı!)"
    )

st.markdown('</div>', unsafe_allow_html=True)

# İşlem türü seçimi
st.markdown('<div class="option-container">', unsafe_allow_html=True)
st.markdown("### 🎯 İşlem Türü Seçin")

process_type = st.radio(
    "Ne yapmak istiyorsunuz?",
    ["📝 Sadece Transkript", "🤖 Sadece AI Özet", "📝🤖 Hem Transkript Hem AI Özet"],
    index=2 if gemini_model else 0,
    help="Sadece ihtiyacınız olan işlemi seçerek süreyi kısaltabilirsiniz"
)

# AI özet için gerekli olan durumlarda Gemini kontrolü
need_ai = "AI Özet" in process_type
if need_ai and not gemini_model:
    st.warning("⚠️ AI özet için Gemini API anahtarı gerekli. Sadece transkript modu kullanılacak.")
    process_type = "📝 Sadece Transkript"

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Video bilgilerini göster
if video_url:
    with st.spinner("📹 Video bilgileri alınıyor..."):
        video_info = get_video_info(video_url)
        st.session_state.video_info = video_info
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

            # 2. Transkripsiyon (gerekirse)
            if "Transkript" in process_type or "AI Özet" in process_type:
                if use_parallel:
                    st.info(f"🚀 Paralel işleme aktif - {chunk_length} dakikalık parçalar")
                    transcript = transcribe_audio_parallel(audio_path, model_name, language_code, chunk_length)
                else:
                    with st.spinner("🧠 Konuşma metne dönüştürülüyor..."):
                        model = load_whisper_model(model_name)
                        result = model.transcribe(
                            audio_path,
                            language=language_code,
                            fp16=False,
                            verbose=False,
                            beam_size=1,
                            best_of=1,
                        )
                        transcript = result['text']
                
                st.session_state.transcript = transcript

            # 3. AI özetleme (gerekirse)
            if "AI Özet" in process_type and gemini_model:
                with st.spinner("🔮 AI özet hazırlanıyor..."):
                    video_title = st.session_state.video_info.get('title', '')
                    summary = analyze_transcript_with_gemini(gemini_model, st.session_state.transcript, video_title)
                    st.session_state.ai_summary = summary
                
                st.markdown('<div class="success-card">✅ AI özet hazır!</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Hata: {str(e)}")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

# Sonuçları göster
if st.session_state.transcript or st.session_state.ai_summary:
    st.markdown("---")
    st.markdown("## 📊 Sonuçlar")
    
    # Layout belirleme
    show_transcript = st.session_state.transcript and ("Transkript" in process_type or not process_type)
    show_summary = st.session_state.ai_summary and ("AI Özet" in process_type or not process_type)
    
    if show_transcript and show_summary:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📝 Ham Transkript")
            st.text_area(
                "transcript_content",
                st.session_state.transcript,
                height=400,
                label_visibility="collapsed",
                key="transcript_display"
            )
            st.download_button(
                "📥 Transkripti İndir",
                data=st.session_state.transcript,
                file_name=f"transkript_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                key="download_transcript"
            )

        with col2:
            st.markdown("### 🤖 AI Özetleme")
            st.markdown(f'<div class="result-container">{st.session_state.ai_summary}</div>', unsafe_allow_html=True)
            
            st.download_button(
                "📥 AI Özetini İndir",
                data=st.session_state.ai_summary,
                file_name=f"ai_ozet_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                key="download_summary"
            )
    
    elif show_transcript:
        st.markdown("### 📝 Ham Transkript")
        st.text_area(
            "transcript_content",
            st.session_state.transcript,
            height=400,
            label_visibility="collapsed",
            key="transcript_display_full"
        )
        col1, col2 = st.columns([1, 3])
        with col1:
            st.download_button(
                "📥 Transkripti İndir",
                data=st.session_state.transcript,
                file_name=f"transkript_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                key="download_transcript_only"
            )
    
    elif show_summary:
        st.markdown("### 🤖 AI Özetleme")
        st.markdown(f'<div class="result-container">{st.session_state.ai_summary}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.download_button(
                "📥 AI Özetini İndir",
                data=st.session_state.ai_summary,
                file_name=f"ai_ozet_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                key="download_summary_only"
            )

# Temizleme butonu
if st.session_state.transcript or st.session_state.ai_summary:
    if st.button("🧹 Sonuçları Temizle"):
        st.session_state.transcript = ""
        st.session_state.ai_summary = ""
        st.session_state.video_info = {}
        st.rerun()

# Alt bilgi
st.markdown("""
---
<div style='text-align:center; color: #718096; font-size: 0.9rem; padding: 2rem 0;'>
    🤖 <strong>Powered by</strong> OpenAI Whisper • Google Gemini 1.5 Flash<br>
    <em>Profesyonel Video Analizi Sistemi</em>
</div>
""", unsafe_allow_html=True)