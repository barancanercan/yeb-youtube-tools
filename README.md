# 🎬 YEB AI YouTube Özetleyici

> **Yapay Zeka Destekli YouTube Video Analizi ve Profesyonel Özetleme Sistemi**

YEB AI YouTube Özetleyici, YouTube videolarından otomatik transkript çıkarma ve yapay zeka destekli profesyonel özetleme sunan gelişmiş bir web uygulamasıdır. OpenAI Whisper ve Google Gemini 1.5 Flash teknolojilerini birleştirerek, video içeriklerini detaylı analizler ve uygulanabilir özetler haline getirir.

## ✨ Özellikler

### 🧠 Gelişmiş AI Teknolojileri
- **OpenAI Whisper**: En gelişmiş konuşma tanıma teknolojisi
- **Google Gemini 1.5 Flash**: Hızlı ve akıllı içerik analizi
- **Paralel İşleme**: Ses dosyalarını parçalara bölerek 3-5x daha hızlı transkripsiyon
- **Çoklu Dil Desteği**: Türkçe, İngilizce, Almanca, Fransızca, İspanyolca

### 📊 Profesyonel Analiz
- **Akıllı Özetleme**: Video içeriğinin temel konularını çıkarma
- **Gündem Analizi**: Güncel olaylarla bağlantı kurma
- **Anahtar Nokta Tespiti**: Önemli bilgi ve argümanları vurgulama
- **Hedef Kitle Analizi**: Pratik uygulama önerileri
- **Esnek Çıktı Seçenekleri**: Sadece transkript, sadece özet veya her ikisi birden

### 🎨 Modern Arayüz
- **Karanlık Tema**: Göz dostu, modern tasarım
- **Responsive Layout**: Tüm cihazlarda mükemmel görünüm
- **Real-time Progress**: Paralel işleme durumu takibi
- **Kolay Kullanım**: Tek tık ile analiz başlatma
- **İndirme Seçenekleri**: TXT ve Markdown formatları

### ⚡ Performans Optimizasyonları
- **Chunk-based Processing**: Ses dosyalarını parçalara böler
- **Thread-safe Operations**: Güvenli paralel işleme
- **Model Caching**: Whisper ve Gemini modellerini cache'ler
- **Memory Management**: Otomatik bellek temizliği
- **Error Recovery**: Graceful hata yönetimi

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.8+
- FFmpeg
- Gemini API Anahtarı (AI özet için)

### Kurulum

1. **Depoyu klonlayın:**
   ```bash
   git clone https://github.com/barancanercan/yeb-youtube-tools.git
   cd yeb-youtube-tools
   ```

2. **Sanal ortam oluşturun:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # veya
   .venv\Scripts\activate     # Windows
   ```

3. **Bağımlılıkları yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```

4. **FFmpeg kurun:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # https://ffmpeg.org/download.html adresinden indirin
   ```

5. **API anahtarını ayarlayın:**
   ```bash
   # Environment variable olarak
   export GEMINI_API_KEY="your-api-key-here"
   
   # Veya .env dosyası oluşturun
   echo "GEMINI_API_KEY=your-api-key-here" > .env
   ```

6. **Uygulamayı başlatın:**
   ```bash
   streamlit run app.py
   ```

## 🔧 Yapılandırma

### Gemini API Anahtarı

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'ya gidin
2. "Create API Key" butonuna tıklayın
3. API anahtarınızı kopyalayın
4. Environment variable veya .env dosyasına ekleyin

### Model Seçenekleri

| Model | Hız | Doğruluk | Kullanım | RAM |
|-------|-----|----------|----------|-----|
| tiny | ⭐⭐⭐⭐⭐ | ⭐⭐ | Test ve hızlı önizleme | ~39 MB |
| base | ⭐⭐⭐⭐ | ⭐⭐⭐ | Günlük kullanım (önerilen) | ~74 MB |
| small | ⭐⭐⭐ | ⭐⭐⭐⭐ | Kaliteli transkript | ~244 MB |
| medium | ⭐⭐ | ⭐⭐⭐⭐⭐ | Profesyonel kullanım | ~769 MB |
| large | ⭐ | ⭐⭐⭐⭐⭐ | Maksimum doğruluk | ~1550 MB |

### Paralel İşleme Ayarları

| Chunk Uzunluğu | Paralel Thread | Hız Artışı | Önerilen Kullanım |
|-----------------|----------------|-------------|-------------------|
| 0.5 dakika | 4x | 4-5x | Uzun videolar (30+ dk) |
| 1 dakika | 3-4x | 3-4x | Orta videolar (10-30 dk) |
| 2 dakika | 2-3x | 2-3x | Kısa videolar (5-15 dk) |
| 3+ dakika | 1-2x | 1-2x | Çok kısa videolar (<10 dk) |

## 📋 Kullanım

### Temel Kullanım
1. YouTube video URL'sini yapıştırın
2. Dil ve model seçimini yapın
3. Çıktı türünü seçin:
   - **📝 Sadece Transkript**: En hızlı seçenek
   - **🤖 Sadece AI Özet**: Özet + transkript (ham metin gösterilmez)
   - **📝🤖 Her İkisi**: Tam özellik
4. Paralel işleme ayarlarını yapın
5. "Analizi Başlat" butonuna tıklayın

### Performans İpuçları
- **Kısa videolar için**: Paralel işlemeyi kapatın
- **Uzun videolar için**: 0.5-1 dakika chunk kullanın
- **Yavaş sistemler için**: tiny/base model seçin
- **Maksimum kalite için**: large model + 2+ dakika chunk

### Çıktı Formatları

#### Ham Transkript
- Zaman sıralı metin
- TXT formatında indirilebilir
- Düzenlenebilir format

#### AI Özetleme
- **📋 Genel Özet**: 2-3 cümlelik ana konu
- **🎯 Ana Konular**: Madde halinde temel başlıklar
- **🔍 Anahtar Noktalar**: Önemli veriler ve iddialar
- **🗞️ Gündem İlişkisi**: Güncel olaylarla bağlantılar
- **💡 Öne Çıkan Alıntılar**: Etkileyici ifadeler
- **📊 Hedef Kitle Analizi**: Pratik uygulamalar

## 🛠️ Teknik Detaylar

### Teknoloji Stack
- **Frontend**: Streamlit
- **Speech-to-Text**: OpenAI Whisper
- **AI Analysis**: Google Gemini 1.5 Flash
- **Video Processing**: yt-dlp + FFmpeg
- **Audio Processing**: pydub
- **Parallel Processing**: concurrent.futures
- **Language**: Python 3.8+

### Sistem Mimarisi
```
YouTube URL → yt-dlp → Audio Extract → Audio Chunks
                                              ↓
                                    Parallel Whisper Processing
                                              ↓
                                    Merge & Clean Transcript
                                              ↓
                                     Gemini 1.5 Flash Analysis
                                              ↓
                                     Professional Summary
```

### Performans Metrikleri

| Video Süresi | Normal İşleme | Paralel İşleme | Hız Artışı |
|--------------|---------------|----------------|-------------|
| 5 dakika     | ~30 saniye    | ~15 saniye     | **2x**      |
| 15 dakika    | ~90 saniye    | ~25 saniye     | **3.6x**    |
| 30 dakika    | ~180 saniye   | ~40 saniye     | **4.5x**    |
| 60 dakika    | ~360 saniye   | ~70 saniye     | **5x**      |

### Güvenlik & Privacy
- API anahtarları environment variable'dan okunur
- Geçici dosyalar otomatik temizlenir
- Thread-safe operations
- No data persistence
- Local processing

## 📁 Proje Yapısı

```
yeb-youtube-tools/
├── app.py                  # Ana uygulama
├── requirements.txt        # Python bağımlılıkları
├── packages.txt           # Sistem bağımlılıkları (deploy için)
├── runtime.txt           # Python version (deploy için)
├── .streamlit/
│   ├── config.toml       # Streamlit yapılandırması
│   └── secrets.toml      # API anahtarları (deploy için)
├── .env.example          # Environment dosyası örneği
├── .gitignore            # Git ignore kuralları
└── README.md             # Bu dosya
```

## 🚢 Deployment

### Streamlit Community Cloud

1. **GitHub'a repository'yi push edin**
2. **[Streamlit Community Cloud](https://streamlit.io/cloud)'a gidin**
3. **Repository'yi bağlayın**
4. **Secrets ekleyin:**
   ```toml
   # .streamlit/secrets.toml
   [general]
   GEMINI_API_KEY = "your_gemini_api_key_here"
   ```
5. **Deploy edin**

### Docker Deployment

```dockerfile
FROM python:3.9-slim

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App files
COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Environment Variables
```bash
# Production environment
GEMINI_API_KEY=your_api_key_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! 

### Development Setup
```bash
git clone https://github.com/barancanercan/yeb-youtube-tools.git
cd yeb-youtube-tools
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Contribution Workflow
1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🆘 Destek & Troubleshooting

### Sık Karşılaşılan Sorunlar

**Q: "ModuleNotFoundError: No module named 'pydub'" hatası alıyorum**
```bash
A: pip install pydub
```

**Q: "FFmpeg eksik" hatası alıyorum**
```bash
# Ubuntu/Debian
A: sudo apt-get install ffmpeg

# macOS
A: brew install ffmpeg

# Windows
A: https://ffmpeg.org/download.html adresinden indirin
```

**Q: Gemini API hatası alıyorum**
```bash
A: API anahtarınızın doğru olduğundan ve aktif olduğundan emin olun
   export GEMINI_API_KEY="your-key-here"
```

**Q: Paralel işleme çalışmıyor**
```bash
A: Python'da threading sorunları olabilir. Paralel işlemeyi kapatıp deneyin.
```

**Q: Memory hatası alıyorum**
```bash
A: Daha küçük model (tiny/base) ve kısa chunk süresi (0.5-1dk) deneyin.
```

### Performance Tuning

**Yavaş Transkripsiyon:**
- Daha küçük model kullanın (tiny/base)
- Chunk süresini azaltın (0.5-1 dakika)
- Paralel işlemeyi aktifleştirin

**Yüksek Memory Kullanımı:**
- tiny/base model kullanın
- Chunk süresini artırın (2-3 dakika)
- Thread sayısını azaltın

**API Rate Limiting:**
- Gemini API kullanım limitlerini kontrol edin
- Daha kısa videolar deneyin
- Batch processing yapmayın

### İletişim
- **GitHub**: [@barancanercan](https://github.com/barancanercan)
- **Issues**: [GitHub Issues](https://github.com/barancanercan/yeb-youtube-tools/issues)
- **Discussions**: [GitHub Discussions](https://github.com/barancanercan/yeb-youtube-tools/discussions)

## 🔮 Roadmap

### v2.0 (Yakında)
- [ ] Batch processing desteği
- [ ] Video timestamp'leri ile bölümlenmiş transkript
- [ ] Podcast desteği (RSS feeds)
- [ ] RESTful API endpoints
- [ ] Claude/ChatGPT integration

### v2.1 (Gelecek)
- [ ] Çoklu format export (PDF, DOCX, JSON)
- [ ] Sosyal medya integration
- [ ] Advanced analytics dashboard
- [ ] Custom prompt templates
- [ ] Multi-language summary support

### v2.2 (İleri)
- [ ] Real-time streaming transcription
- [ ] Speaker identification
- [ ] Sentiment analysis
- [ ] Topic clustering
- [ ] Video search & indexing

---

<div align="center">

**🤖 Powered by OpenAI Whisper • Google Gemini 1.5 Flash • YEB AI Labs**

*Profesyonel Video Analizi ve İçerik Özetleme Sistemi*

[![Made with ❤️](https://img.shields.io/badge/Made%20with-❤️-red.svg)](https://github.com/barancanercan/yeb-youtube-tools)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Made with ❤️ by [Baran Can ERCAN](https://github.com/barancanercan)

</div>