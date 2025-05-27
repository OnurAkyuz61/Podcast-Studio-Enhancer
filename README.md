# Podcast Studio Enhancer

## Proje Hakkında

Podcast Studio Enhancer, normal ses kayıtlarını profesyonel stüdyo kalitesinde podcast kayıtlarına dönüştüren bir masaüstü uygulamasıdır. Uygulama, kullanıcı dostu bir arayüz ile herhangi bir ses kaydını yüksek kaliteli podcast formatına otomatik olarak dönüştürebilir.

Geliştirici: Onur Akyüz

## Özellikler

- **Kolay Kullanım**: Kullanıcı dostu, modern ve koyu temalı arayüz
- **Sürükle ve Bırak**: Ses dosyalarını kolayca yükleme
- **Otomatik Ses İyileştirme**: Tek tıkla profesyonel kaliteye dönüştürme
- **Gürültü Azaltma**: Arka plan gürültülerini temizleme
- **Ses Seviyesi Normalleştirme**: Dengeli ses seviyesi ayarlama
- **EQ Profilleri**: Çeşitli EQ profilleri (Doğal, Sıcak, Parlak, Derin, Özel)
- **Kompresyon**: Dinamik aralık sıkıştırma ve ses yoğunluğunu artırma
- **İlerleme Penceresi**: İşlem sırasında popup ilerleme çubuğu
- **Kolay Dışa Aktarma**: İşlenmiş dosyaları otomatik olarak kaydetme

## Proje Yapısı

Proje, modular bir yapıda tasarlanmıştır ve aşağıdaki klasör yapısına sahiptir:

```
podcast-edit-app/
├── assets/              # Uygulama için gerekli görsel ve medya dosyaları
├── output/              # İşlenmiş ses dosyalarının kaydedildiği klasör
├── resources/           # Ek kaynaklar
├── src/                 # Kaynak kodları
│   ├── __init__.py
│   ├── audio_processing/  # Ses işleme modülleri
│   │   ├── __init__.py
│   │   └── processor.py    # Ana ses işleme sınıfı
│   ├── ui/                # Kullanıcı arayüzü modülleri
│   │   ├── __init__.py
│   │   ├── drag_drop_area.py # Sürükle-bırak alanı bileşeni
│   │   └── main_window.py    # Ana pencere sınıfı
│   └── utils/              # Yardımcı fonksiyonlar
│       └── __init__.py
├── main.py              # Uygulamanın giriş noktası
├── README.md            # Proje dokumantasyonu
└── requirements.txt     # Gerekli Python kütüphaneleri
```

## Teknik Detaylar

### Kullanılan Teknolojiler

- **Python**: Ana programlama dili
- **Tkinter**: Grafik kullanıcı arayüzü (GUI) için
- **Librosa**: Ses analizi ve işleme
- **NumPy & SciPy**: Bilimsel hesaplamalar ve sinyal işleme
- **Soundfile**: Ses dosyalarını okuma ve yazma
- **Pydub**: Ses formatı dönüştürme
- **Noisereduce**: Gürültü azaltma algoritması

### Modüller ve Sınıflar

#### 1. Ana Modül (main.py)

Uygulamanın başlangıç noktasıdır. Tkinter uygulamasını başlatır, ana pencereyi oluşturur ve gerekli stil ayarlarını yapar.

#### 2. Kullanıcı Arayüzü (src/ui/)

- **MainWindow**: Ana uygulama penceresini ve tüm kontrolleri içerir.
- **AudioDropArea**: Ses dosyalarını sürükle-bırak ile yükleme alanını sağlar.
- **ProcessingThread**: Ses işleme işlemlerini arka planda çalıştıran iş parçacığı (thread).

#### 3. Ses İşleme (src/audio_processing/)

- **AudioProcessor**: Tüm ses işleme fonksiyonlarını içeren ana sınıf.
  - Gürültü azaltma
  - EQ uygulama
  - Kompresyon
  - Ses seviyesi normalleştirme
  - Format dönüştürme

## Kurulum

### Gereksinimler

- Python 3.8 veya üstü
- pip (Python paket yöneticisi)

### Adımlar

1. Python kütüphanelerini yükleyin:

```bash
pip install -r requirements.txt
```

2. FFmpeg yüklenmesi (MP3 dönüşümü için gerekli):

**macOS (Homebrew ile):**
```bash
brew install ffmpeg
```

**Windows:**
```
https://ffmpeg.org/download.html adresinden FFmpeg indirip yükleyin ve PATH'e ekleyin.
```

**Linux:**
```bash
sudo apt-get install ffmpeg  # Debian/Ubuntu
sudo yum install ffmpeg      # CentOS/RHEL
```

**Not:** FFmpeg yüklü değilse, program çalışmaya devam edecek ancak ses dosyaları WAV formatında kaydedilecektir (MP3 yerine).

## Kullanım

1. Uygulamayı başlatın:

```bash
python main.py
```

2. Ses dosyası yükleme:
   - Sürükle-bırak alanına bir ses dosyası sürükleyin veya
   - "Ses Dosyası Seç" butonuna tıklayarak bir dosya seçin

3. İyileştirme ayarlarını yapın:
   - Gürültü Azaltma: Gürültü azaltma seviyesini ayarlayın (0-100%)
   - Kompresyon: Ses kompresyon miktarını ayarlayın (0-100%)
   - EQ Profili: Ses karakterini belirleyen profili seçin

4. "İyileştirmeyi Başlat" butonuna tıklayın

5. İşlem sırasında popup ilerleme penceresi görüntülenecektir

6. İşlem tamamlandığında, iyileştirilmiş ses dosyası "output" klasörüne kaydedilecektir

## Ses İyileştirme İşlemi

Uygulama, ses dosyasını aşağıdaki adımlarla işler:

1. **Ses Yükleme**: Dosya yüklenir ve ses verisi okunur
2. **Gürültü Azaltma**: Arka plan gürültüsü temizlenir
3. **EQ Uygulama**: Seçilen profile göre frekans bantları ayarlanır
4. **Kompresyon**: Dinamik aralık sıkıştırılır
5. **Normalleştirme**: Ses seviyesi optimize edilir
6. **Kaydetme**: İşlenmiş ses dosyası kaydedilir
7. **Format Dönüştürme**: Eğer FFmpeg yüklüyse, WAV dosyası MP3'e dönüştürülür

## EQ Profilleri

Uygulama şu EQ profillerini sunar:

- **Stüdyo**: Profesyonel stüdyo kalitesinde ses için optimize edilmiş ayar (varsayılan)
- **Doğal**: Hafif orta frekans artışı ile net ses
- **Sıcak**: Alttaki frekansları artırarak sıcak bir ton
- **Parlak**: Yüksek frekansları artırarak parlak ve net ses
- **Derin**: Bas frekansları artırarak derin ve güçlü ses
- **Özel**: Dengeli bir EQ ayarı

## Geliştirme

Projeyi geliştirmek veya katkıda bulunmak isterseniz:

1. Projeyi klonlayın
2. Gerekli bağımlılıkları yükleyin
3. Yeni özellikler ekleyin veya hata düzeltmeleri yapın
4. Pull request gönderin

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.