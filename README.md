# PlateGuard 🇹🇷 🚗

**PlateGuard**, Türkiye'deki standart araç plakaları ile modifiye / yasadışı (APP - Avrupa Press Plaka) plakaları birbirinden ayırt etmek için tasarlanmış, **Yapay Zeka Destekli (YOLOv11 + Moondream2 VLM)** bir görüntü tanıma sistemidir.

Proje, özellikle **AMD ROCm / Ollama** vb. yerel VLM donanım hızlandırmalarını kullanarak görüntü işleme ve detaylı görsel çıkarım (Visual Language Modeling) yapar.

---

## 🚀 Başlangıç Seçenekleri

### Seçenek 1: GitHub Codespaces (En Kolay - Önerilen!) ⭐

**Hiç kurulum yapmanıza gerek yok!**

1. Repoyu açıp yeşil **"< > Code"** butonuna tıklayın
2. **"Codespaces"** sekmesini seçin  
3. **"Create codespace on main"** düğmesine basın
4. 2-3 dakika bekleyin (ortam otomatik kurulur)
5. Terminal'de şunu çalıştırın:
```bash
docker run -d --name ollama -p 11434:11434 ollama/ollama
docker exec ollama ollama pull moondream
streamlit run app.py
```

**Bam! 🎉** Tarayıcıda otomatik açılacak.

---

### Seçenek 2: Kendi Bilgisayarınızda Çalıştırma

#### Gereksinimler
- **Python 3.8+**
- **Ollama** (https://ollama.com/download)
- **Git**

#### Adımlar

**1. Repoyu klonlayın:**
```bash
git clone https://github.com/ugur-demirkaya/PlateGuard.git
cd PlateGuard
```

**2. Python paketlerini yükleyin:**
```bash
pip install -r requirements.txt
```

**3. Ollama'yı başlatın (Arkaplanda):**
```bash
ollama serve
```

**4. Başka bir terminal penceresinde Moondream modelini indirin:**
```bash
ollama pull moondream
```

**5. Uygulamayı çalıştırın:**
```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

---

## 📋 Özellikler

- **Hassas Plaka Algılama:** HuggingFace altyapılı (`morsetechlab/yolov11-license-plate-detection`) fine-tune edilmiş YOLOv11 modeli kullanılarak resimdeki tam plaka lokasyonu ve birden fazla plaka eşzamanlı olarak tespit edilir.
- **Otomatik Kırpma (Auto-Crop):** Geniş çerçeveden sadece hedeflenen plakalar sınır paylarıyla (padding) kırpılıp analize hazır hale getirilir.
- **Micro-VLM ile Derin Analiz:** Kırpılan plaka görüntüleri yerel ağda (localhost:11434) koşan Ollama modeline (**Moondream2 / LLaVA vb.**) beslenir ve tipografi büyüklüğü, kanal derinliği vb. faktörlere göre "APP" vs "Standart" sınıflandırması yapılır.
- **Streamlit Web Arayüzü:** Kullanıcı dostu web arayüzü sayesinde kolay görüntü yükleme, anlık işlem raporu ve yan yana plaka analiz sonuçları.

## 🛠️ Teknoloji Stack

| Bileşen | Teknoloji |
|---------|-----------|
| **Plaka Tespiti** | YOLOv11 (Fine-Tuned) |
| **Sınıflandırma** | Moondream2 VLM |
| **Model Servesi** | Ollama (Local Inference) |
| **Web Arayüzü** | Streamlit |
| **Görüntü İşleme** | OpenCV, PIL, NumPy |
| **Framework** | Python 3.x |

---

## 🏗️ Mimari

```
┌──────────────────────────────────────────┐
│   Kullanıcı: Araç Fotoğrafı Yükle       │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  YOLOv11 (Fine-Tuned)                   │
│  ├─ Plaka Bölgesi Tespiti               │
│  └─ Bounding Box Çıkartma & Kırpma      │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Moondream2 VLM (Ollama)                 │
│  ├─ Font Kalınlığı Analizi               │
│  ├─ Karakter Şekli Kontrolü              │
│  └─ APP vs Standart Karar                │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Sonuç Ekranı                           │
│  ✓ APP Plaka / Standart Plaka           │
│  ✓ Güven Yüzdesi                        │
│  ✓ Detaylı Açıklama                     │
└──────────────────────────────────────────┘
```

---

## 📸 Nasıl Kullanılır?

1. **Fotoğraf Yükle:** Araç plakasının görüldüğü bir JPG/PNG yükleyin
2. **Otomatik İşlem:** Sistem otomatik olarak:
   - Plakaları tespit eder
   - Görüntüyü kırpar
   - VLM ile analiz eder
3. **Sonuç Görün:** APP mı Standart mı olduğunu anlık olarak görebilirsiniz

---

## ⚠️ Notlar

- **İlk Çalıştırma:** Modeller ilk kez indirildiğinde biraz zaman alabilir (2-3 dakika)
- **Donanım:** Codespaces CPU kullanır. Daha hızlı işlem için lokal makinenizde Ollama'yı GPU ile çalıştırabilirsiniz
- **Model Boyutu:** Moondream (~2GB) ve YOLOv11 (~100MB) depolama gerektirir
- **Ollama Versiyonu:** En son Ollama sürümünü kullanmanız önerilir

---

## 🔧 Sorun Giderme

### "ollama: command not found"
Lokal makinede çalıştırıyorsanız, Ollama'yı indirip kurun: https://ollama.com/download

### "Connectionrefused to localhost:11434"
Ollama servisinin çalışıp çalışmadığını kontrol edin:
```bash
ollama serve  # Yeni terminal penceresinde çalıştırın
```

### "Port 11434 already in use"
Başka bir Ollama örneği çalışıyor. Öldürün veya portu değiştirin:
```bash
# Lokal
lsof -i :11434
kill -9 <PID>

# Codespaces Docker
docker kill ollama
docker run -d --name ollama -p 11434:11434 ollama/ollama
```

---

## 📚 Daha Fazla Bilgi

- [Ollama Resmi Sitesi](https://ollama.com)
- [Moondream GitHub](https://github.com/vikhyat/moondream)
- [YOLOv11 Ultralytics](https://docs.ultralytics.com/models/yolov11/)
- [Streamlit Dokümantasyonu](https://docs.streamlit.io)

---

## 📄 Lisans

Bu proje açık kaynaktır. Lütfen katkılarınız için PR gönderin!

---

**Sorularınız mı var? GitHub Issues'de bize ulaşın! 💬**
