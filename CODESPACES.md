# GitHub Codespaces & DevContainer İçin Kurulum

## Codespaces Üzerinde 1-Tıkla Çalıştırma

Bu repo, GitHub Codespaces'te **tam otomatik** bir ortamda çalıştırılması için yapılandırılmıştır.

### 🚀 Hızlı Başlangıç (Codespaces)

1. Repoyu açıp "**Code**" butonuna tıklayın
2. "**Codespaces**" sekmesinde "**Create codespace on main**" düğmesine basın
3. Codespaces otomatik olarak:
   - ✅ Python kütüphanelerini yükleyecek (`pip install -r requirements.txt`)
   - ✅ Ollama'yı kuracak
   - ✅ Moondream2 modelini çekecek
   - ✅ VS Code uzantılarını yükleyecek

4. Ortam hazır olduktan sonra terminal'de:
   ```bash
   ollama serve &  # Ollama servisini arkaplanda başlat
   streamlit run app.py  # Uygulamayı çalıştır
   ```

5. Tarayıcı otomatik olarak `http://localhost:8501` adresine yönlendirilecektir.

### 📋 Yapılandırma Detayları (`.devcontainer/devcontainer.json`)

- **Base Image:** Python 3.10 (Debian Bullseye)
- **Otomatik Kurulum:** Tüm pip paketleri otomatik yükleniyor
- **Ollama:** Linux üzerinde saydam kurulu hale geliyor
- **Port Forwarding:** 
  - `8501` → Streamlit UI
  - `11434` → Ollama API
- **VS Code Extensions:** Pylance, Ruff, Python vb. otomatik yükleniyor

### ⚠️ Notlar

- **İlk Başlangıç:** Container oluşturken ve Moondream modeli indirilirken (1-2 dakika) biraz zaman alabilir.
- **Donanım:** Codespaces default CPU verir (GPU yok). Yine de çalışır ancak sizin bilgisayarınızdan daha yavaş olacaktır.
- **Model Boyutu:** Moondream (~2GB) indirildikten sonra container depolama kullanır.

### 🏠 Lokal Çalıştırma (Kendi Bilgisayarınızda)

```bash
pip install -r requirements.txt
ollama serve &  # Arka planda koştur
streamlit run app.py
```

Eğer Ollama hali hazırda kurul değilse: https://ollama.com/download
