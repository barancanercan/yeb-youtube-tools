# 🎬 YEB AI YouTube Özetleyici

> **Yapay Zeka Destekli YouTube Video Analizi ve Profesyonel Özetleme Sistemi**

YEB AI YouTube Özetleyici, YouTube videolarından otomatik transkript çıkarma ve yapay zeka destekli profesyonel özetleme sunan gelişmiş bir web uygulamasıdır. OpenAI Whisper ve Google Gemini 1.5 Flash teknolojilerini birleştirerek, video içeriklerini detaylı analizler ve uygulanabilir özetler haline getirir.

## ✨ Özellikler

### 🧠 Gelişmiş AI Teknolojileri
- **OpenAI Whisper**: En gelişmiş konuşma tanıma teknolojisi
- **Google Gemini 1.5 Flash**: Hızlı ve akıllı içerik analizi
- **Çoklu Dil Desteği**: Türkçe, İngilizce, Almanca, Fransızca, İspanyolca

### 📊 Profesyonel Analiz
- **Akıllı Özetleme**: Video içeriğinin temel konularını çıkarma
- **Gündem Analizi**: Güncel olaylarla bağlantı kurma
- **Anahtar Nokta Tespiti**: Önemli bilgi ve argümanları vurgulama
- **Hedef Kitle Analizi**: Pratik uygulama önerileri

### 🎨 Modern Arayüz
- **Karanlık Tema**: Göz dostu, modern tasarım
- **Responsive Layout**: Tüm cihazlarda mükemmel görünüm
- **Kolay Kullanım**: Tek tık ile analiz başlatma
- **İndirme Seçenekleri**: TXT ve Markdown formatları

## 🚀 Hızlı Başlangıç

### Gereksinimler
- Python 3.8+
- FFmpeg
- Gemini API Anahtarı

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
   # https://ffmpeg.org/download.html
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

| Model | Hız | Doğruluk | Kullanım |
|-------|-----|----------|----------|
| tiny | ⭐⭐⭐⭐⭐ | ⭐⭐ | Test ve hızlı önizleme |
| base | ⭐⭐⭐⭐ | ⭐⭐⭐ | Günlük kullanım (önerilen) |
| small | ⭐⭐⭐ | ⭐⭐⭐⭐ | Kaliteli transkript |
| medium | ⭐⭐ | ⭐⭐⭐⭐⭐ | Profesyonel kullanım |
| large | ⭐ | ⭐⭐⭐⭐⭐ | Maksimum doğruluk |

## 📋 Kullanım

### Temel Kullanım
1. YouTube video URL'sini yapıştırın
2. Dil ve model seçimini yapın
3. AI Özet seçeneğini aktifleştirin
4. "Analizi Başlat" butonuna tıklayın

### Çıktı Formatları

#### Ham Transkript
- Zaman damgalı metin
- TXT formatında indirilebilir
- Düzenlenebilir format

#### AI Özetleme
- **Genel Özet**: 2-3 cümlelik ana konu
- **Ana Konular**: Madde halinde temel başlıklar
- **Anahtar Noktalar**: Önemli veriler ve iddialar
- **Gündem İlişkisi**: Güncel olaylarla bağlantılar
- **Öne Çıkan Alıntılar**: Etkileyici ifadeler
- **Hedef Kitle Analizi**: Pratik uygulamalar

## 🛠️ Teknik Detaylar

### Teknoloji Stack
- **Frontend**: Streamlit
- **Speech-to-Text**: OpenAI Whisper
- **AI Analysis**: Google Gemini 1.5 Flash
- **Video Processing**: yt-dlp + FFmpeg
- **Language**: Python 3.8+

### Sistem Mimarisi
```
YouTube URL → yt-dlp → Audio Extract → Whisper → Transcript
                                              ↓
                                     Gemini 1.5 Flash
                                              ↓
                                     Professional Summary
```

### Güvenlik
- API anahtarları environment variable'dan okunur
- Geçici dosyalar otomatik temizlenir
- Güvenli HTTP bağlantıları
- Input validasyonu

## 📁 Proje Yapısı

```
yeb-youtube-tools/
├── app.py                  # Ana uygulama
├── requirements.txt        # Python bağımlılıkları
├── packages.txt           # Sistem bağımlılıkları
├── .env.example          # Environment dosyası örneği
├── .gitignore            # Git ignore kuralları
└── README.md             # Bu dosya
```

## 🚢 Deployment

### Streamlit Community Cloud
1. GitHub'a repository'yi push edin
2. [Streamlit Community Cloud](https://streamlit.io/cloud)'a gidin
3. Repository'yi bağlayın
4. Environment variable'ları ekleyin
5. Deploy edin

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz! 

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🆘 Destek

### Sık Karşılaşılan Sorunlar

**Q: "ModuleNotFoundError: No module named 'dotenv'" hatası alıyorum**
A: `pip install python-dotenv` komutunu çalıştırın veya `.env` dosyasını kullanmak yerine environment variable kullanın.

**Q: "FFmpeg eksik" hatası alıyorum**
A: FFmpeg'i sisteminize kurun. [FFmpeg İndirme Sayfası](https://ffmpeg.org/download.html)

**Q: Gemini API hatası alıyorum**
A: API anahtarınızın doğru olduğundan ve aktif olduğundan emin olun.

### İletişim
- **GitHub**: [@barancanercan](https://github.com/barancanercan)
- **Issues**: [GitHub Issues](https://github.com/barancanercan/yeb-youtube-tools/issues)
- **E-posta**: İletişim için GitHub profilini ziyaret edin

## 🔮 Gelecek Planları

### v2.0 (Yakında)
- [ ] Batch processing desteği
- [ ] Video timestamp'leri
- [ ] Podcast desteği
- [ ] API endpoint'leri

### v2.1
- [ ] Çoklu format export (PDF, DOCX)
- [ ] Sosyal medya integration
- [ ] Advanced analytics dashboard

---

<div align="center">

**🤖 Powered by OpenAI Whisper • Google Gemini 1.5 Flash • YEB AI Labs**

*Profesyonel Video Analizi ve İçerik Özetleme Sistemi*

Made with ❤️ by [Baran Can ERCAN](https://github.com/barancanercan)

</div>