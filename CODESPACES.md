# GitHub Codespaces & DevContainer İçin Kurulum

## Codespaces Üzerinde 1-Tıkla Çalıştırma

Bu repo, GitHub Codespaces'te **tam otomatik** bir ortamda çalıştırılması için yapılandırılmıştır.

### 🚀 Hızlı Başlangıç (Codespaces)

1. Repoyu açıp "**Code**" butonuna tıklayın
2. "**Codespaces**" sekmesinde "**Create codespace on main**" düğmesine basın
3. Codespaces otomatik olarak:
   - ✅ Python kütüphanelerini yükleyecek (`pip install -r requirements.txt`)
   - ✅ VS Code uzantılarını yükleyecek

4. **Ollama Kurulumu (Codespaces'te):**

   > ⚠️ **Not:** Codespaces hafif bir ortam olduğu için Ollama'nın binary'sini tam kurmak zor olabilir. İki seçeneğiniz var:
   
   **Seçenek A: Ollama Docker Container'ı (Önerilen)**
   ```bash
   docker run -d -p 11434:11434 ollama/ollama
   # Modeli indir
   docker exec $(docker ps -q) ollama pull moondream
   # Başka bir terminal'de Streamlit'i çalıştır:
   streamlit run app.py
   ```

   **Seçenek B: Manuel Ollama Kurulumu**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama serve
   # Başka bir terminal sekmesinde:
   ollama pull moondream
   streamlit run app.py
   ```

5. Tarayıcı otomatik olarak `http://localhost:8501` adresine yönlendirilecektir.

### 📋 Yapılandırma Detayları (`.devcontainer/devcontainer.json`)

- **Base Image:** Python 3.10 (Debian Bullseye)
- **Otomatik Kurulum:** Tüm pip paketleri otomatik yükleniyor
- **Docker Support:** Docker-in-Docker aktif (Ollama container çalıştırmak için)
- **Port Forwarding:** 
  - `8501` → Streamlit UI
  - `11434` → Ollama API
- **VS Code Extensions:** Pylance, Ruff, Python vb. otomatik yükleniyor

### ⚠️ Notlar

- **İlk Başlangıç:** Container oluşturken 1-2 dakika zaman alabilir.
- **Donanım:** Codespaces default CPU verir (GPU yok). Yine de çalışır ancak sizin bilgisayarınızdan daha yavaş olacaktır.
- **Model Boyutu:** Moondream (~2GB) indirildikten sonra container depolama kullanır.
- **Ollama Sunucusu:** En kolay sürüm Docker ile çalıştırmaktır (Seçenek A).

### 🏠 Lokal Çalıştırma (Kendi Bilgisayarınızda)

```bash
pip install -r requirements.txt
ollama serve &  # Arka planda koştur
streamlit run app.py
```

Eğer Ollama hali hazırda kuruluysa: https://ollama.com/download
