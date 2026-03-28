# PlateGuard 🇹🇷 🚗

**PlateGuard**, Türkiye'deki standart araç plakaları ile modifiye / yasadışı (APP - Avrupa Press Plaka) plakaları birbirinden ayırt etmek için tasarlanmış, **Yapay Zeka Destekli (YOLOv11 + Moondream2 VLM)** bir görüntü tanıma sistemidir.

Proje, özellikle **AMD ROCm / Ollama** vb. yerel VLM donanım hızlandırmalarını kullanarak görüntü işleme ve detaylı görsel çıkarım (Visual Language Modeling) yapar.

## ⚡ En Kolay Başlangıç: GitHub Codespaces (1-Tıkla!)

**Hiçbir kurulum yapmanıza gerek yok!** Repoyu açıp:

1. Yeşil **"< > Code"** butonuna tıklayın
2. **"Codespaces"** sekmesini seçin  
3. **"Create codespace on main"** düğmesine basın
4. 2 dakika bekleyin (ortam otomatik kurulur)
5. Terminal'de şunu çalıştırın:
   ```bash
   docker run -d -p 11434:11434 ollama/ollama
   docker exec $(docker ps -q) ollama pull moondream
   streamlit run app.py
   ```

**Bam! 🚀** Tarayıcıda otomatik açılacak. Hazır!

---

## 📖 Ayrıntılı Rehber

### Codespaces Hakkında Daha Fazla Bilgi
👉 [CODESPACES.md](CODESPACES.md) dosyasını okuyun.

## Özellikler
- **Hassas Plaka Algılama:** HuggingFace altyapılı (`morsetechlab/yolov11-license-plate-detection`) fine-tune edilmiş YOLOv11 modeli kullanılarak resimdeki tam plaka lokasyonu ve birden fazla plaka eşzamanlı olarak tespit edilir.
- **Otomatik Kırpma (Auto-Crop):** Geniş çerçeveden sadece hedeflenen plakalar sınır paylarıyla (padding) kırpılıp analize hazır hale getirilir.
- **Micro-VLM ile Derin Analiz:** Kırpılan plaka görüntüleri yerel ağda (localhost:11434) koşan Ollama modeline (**Moondream2 / LLaVA vb.**) beslenir ve tipografi büyüklüğü, kanal derinliği, mühür olup olmaması gibi "APP" vs "Standart" faktörlerine göre analiz edilir.
- **Streamlit Web Arayüzü:** Kullanıcı dostu web arayüzü sayesinde kolay görüntü yükleme, anlık işlem raporu (`spinner` bildirimleri) ve yan yana plaka analiz sonuçları sağlar.

## Kullanılan Teknolojiler
* **Python 3.x**
* **Streamlit** (UI / Frontend)
* **Ultralytics (YOLOv11)** (Nesne / Plaka Tespiti)
* **Ollama** (Yerel model inference - Moondream2)
* **OpenCV & PIL** (Görüntü İşleme)

## 🏠 Lokal Makinenizde Çalıştırma

### Gereksinimler
- Python 3.8+
- [Ollama](https://ollama.com/download)

### Adımlar

1. **Repoyu Klonlayın:**
```bash
git clone https://github.com/ugur-demirkaya/PlateGuard.git
cd PlateGuard
```

2. **Gerekli Python Paketlerini Yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Ollama'yı Başlatın (Arkaplanda):**
```bash
ollama serve &
```

4. **Moondream Modelini İndirin (İlk Çalıştırma):**
```bash
ollama pull moondream
```

5. **Uygulamayı Çalıştırın:**
```bash
streamlit run app.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

---

## 📝 Mimari

```
┌─────────────────────────────────────────────────┐
│         Kullanıcı: Fotoğraf Yükle             │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│   YOLOv11 (Fine-Tuned) → Plaka Tespiti        │
│   ✓ Bounding Box Çıkartma                     │
│   ✓ Otomatik Kırpma (Auto-Crop)               │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│   Moondream2 VLM (Ollama) → Sınıflandırma     │
│   ✓ Prompt Engineering ile Font Analizi       │
│   ✓ APP vs Standart Karar                     │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│   Sonuç: İki Ayrı Sınıflandırma Çıktısı       │
│   APP Plaka / Standart Plaka                  │
└─────────────────────────────────────────────────┘
```

---

*Bu proje, makine öğrenmesi destekli görüntü sınıflandırma ve plaka tanıma yeteneklerini modern web teknolojileri ile bir araya getirerek hızlı ve esnek bir mimari sunar.*

---

## 🔗 Linkler
- [GitHub](https://github.com/ugur-demirkaya/PlateGuard)
- [CODESPACES Rehberi](CODESPACES.md)
- [Ollama Resmi Sitesi](https://ollama.com)
