# yeb-youtube-tools

YouTube videolarından kolayca transkript almak için Streamlit tabanlı bir araç.

## Özellikler
- YouTube video URL'sinden ses indirir
- OpenAI Whisper ile otomatik transkript oluşturur
- Türkçe, İngilizce, Almanca, Fransızca, İspanyolca dil desteği
- Farklı Whisper model seçenekleri (tiny, base, small, medium, large)
- Sonuçları kolayca kopyala veya indir

## Kurulum
1. Depoyu klonlayın:
   ```bash
   git clone https://github.com/barancanercan/yeb-youtube-tools.git
   cd yeb-youtube-tools
   ```
2. Sanal ortam oluşturun ve aktif edin:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. FFmpeg kurulu olmalı:
   ```bash
   ffmpeg -version
   # Eğer yüklü değilse:
   sudo apt-get install ffmpeg
   ```

## Kullanım
```bash
streamlit run app.py
```
Tarayıcıda açılan adrese gidin ve YouTube video URL'sini girerek transkript alın.

## Deploy
Projeyi Streamlit Community Cloud'a yükleyerek kolayca yayınlayabilirsiniz.

## Lisans
MIT
