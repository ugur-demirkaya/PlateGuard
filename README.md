# PlateGuard 🇹🇷 🚗

**PlateGuard**, Türkiye'deki standart araç plakaları ile modifiye / yasadışı (APP - Avrupa Press Plaka) plakaları birbirinden ayırt etmek için tasarlanmış, **Yapay Zeka Destekli (YOLOv11 + Moondream2 VLM)** bir görüntü tanıma sistemidir.

Proje, özellikle **AMD ROCm / Ollama** vb. yerel VLM donanım hızlandırmalarını kullanarak görüntü işleme ve detaylı görsel çıkarım (Visual Language Modeling) yapar.

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

## Kurulum ve Çalıştırma

1. **Repoyu Klonlayın:**
```bash
git clone https://github.com/ugur-demirkaya/PlateGuard.git
cd PlateGuard
```

2. **Gerekli Kütüphaneleri Yükleyin:**
```bash
pip install -r requirements.txt
```

3. **Ollama Sunucusunu Başlatın:**
Terminal veya komut satırınızda Ollama'nın çalıştığından (ve içinde `moondream` vb. modelin yüklü olduğundan) emin olun:
```bash
ollama serve
# Eğer model inik değilse başka bir terminal sekmesinde:
# ollama pull moondream
```

4. **Uygulamayı Çalıştırın:**
```bash
streamlit run app.py
```

---

*Bu proje, makine öğrenmesi destekli görüntü sınıflandırma ve plaka tanıma yeteneklerini modern web teknolojileri ile bir araya getirerek hızlı ve esnek bir mimari sunar.*
