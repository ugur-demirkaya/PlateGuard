import streamlit as st
import requests
import base64
from PIL import Image
import cv2
import numpy as np
import io
from plate_detector import PlateDetector, crop_plate_region

# Sayfa Ayarları
st.set_page_config(page_title="APP Plaka Dedektörü", layout="wide", page_icon="🚗")

st.title("Türkiye APP vs. Standart Plaka Sınıflandırma Sistemi 🇹🇷")
st.markdown("""
Bu proje, araç fotoğraflarındaki plakaları YZ ile tespit edip, **Ollama VLM Modelleri** kullanarak 
**'APP Plaka'** mı yoksa **'Standart Plaka'** mı olduğunu analiz eder.
""")

# Özel YOLO Plaka Modelini Yükle
@st.cache_resource(show_spinner=False)
def load_plate_detector():
    return PlateDetector()

plate_detector = load_plate_detector()

# Ollama Bağlantısı Kontrol Et
try:
    r = requests.get("http://localhost:11434/api/tags")
    available_models = [m["name"] for m in r.json().get("models", [])]
except:
    available_models = []
    st.error("❌ Ollama sunucusu çalışmıyor! `ollama serve` komutunu çalıştırın.")

if available_models:
    st.sidebar.success(f"✅ Ollama Bağlantısı Kuruldu!")
    st.sidebar.info(f"📦 Mevcut Modeller:\n" + "\n".join(f"- {m}" for m in available_models))

# Model Seçimi
model_choice = st.sidebar.selectbox(
    "Kullanılacak Modelini Seçin:",
    available_models if available_models else ["moondream"],
    help="Ollama'dan indirilen modelleri seç"
)

# Resim Yükleme
uploaded_file = st.file_uploader("Araç Fotoğrafını Yükleyin", type=["jpg", "jpeg", "png", "webp"])

def analyze_with_ollama(image, model):
    """Ollama API'ye resim gönder ve cevap al."""
    # Resmi base64'e çevir
    img_buffer = io.BytesIO()
    image.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    image_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    prompt = """This is a Turkish vehicle license plate. Please analyze the following:
1. Are the characters (letters and numbers) bolder/thicker than standard?
2. Are the character edges sharp and angular, or rounded?
3. Are the characters closer together than normal?
4. Is there a blue European strip with 'TR' marking on the left side?
5. Does the plate look official with proper seal/hologram marks?

If the font is very bold, edges are sharp/angular, and characters are tightly spaced, classify as 'APP Plate' (illegal aftermarket plate).
If everything looks standard and official, classify as 'Standard Plate'.

Reply with EXACTLY this format:
CLASS: [APP Plate / Standard Plate]
CONFIDENCE: [%]
DETAIL: [explanation]"""
    
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "images": [image_base64],
            "stream": False
        }
        
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Cevap alınamadı.")
        else:
            return f"Hata: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    
    st.subheader("📷 Orijinal Görüntü")
    st.image(image, use_container_width=True)

    # Plaka Tespiti
    with st.spinner("Plaka bölgesi tespit ediliyor (YOLOv11 Fine-Tuned Model)..."):
        plates = plate_detector.detect_plates(image)
        
        if not plates:
            st.warning("❗ Otomatik plaka tespiti başarısız oldu. Tam fotoğraf analiz edilecek.")
            st.subheader(f"🔍 {model_choice} ile Tam Fotoğraf Analizi")
            
            with st.spinner(f"🚀 Ollama [{model_choice}] analiz ediyor..."):
                result = analyze_with_ollama(image, model_choice)
                if isinstance(result, str):
                    st.success(f"**Sonuç:**\n\n{result}")
                    if "APP" in str(result).upper():
                        st.snow()
                        st.warning("🚗 **SİSTEMİN KARARI: APP PLAKA** (Modifiye / Özel)")
                    elif "STANDARD" in str(result).upper() or "STANDART" in str(result).upper():
                        st.info("📋 **SİSTEMİN KARARI: STANDART PLAKA** (Resmi)")
                else:
                    st.error(f"Beklenmeyen bir sonuç döndü: {result}")
        else:
            st.success(f"✅ Görüntüde toplam {len(plates)} adet plaka tespit edildi!")
            st.markdown("---")
            
            for idx, p in enumerate(plates):
                st.subheader(f"🔍 Plaka #{idx+1} (Güven Skoru: {p.confidence:.2f})")
                
                # Resim kenarlarına vurmamak için
                padding = 10
                x1, y1, x2, y2 = p.bbox
                x1 = max(0, x1 - padding)
                y1 = max(0, y1 - padding)
                x2 = min(image.width, x2 + padding)
                y2 = min(image.height, y2 + padding)
                
                if x2 > x1 and y2 > y1:
                    plate_img = image.crop((x1, y1, x2, y2))
                    
                    col_img, col_res = st.columns([1, 2])
                    with col_img:
                        st.image(plate_img, use_container_width=True, caption=f"Kırpılan Plaka #{idx+1}")
                    
                    with col_res:
                        with st.spinner(f"🚀 Ollama [{model_choice}] bu plakayı analiz ediyor..."):
                            result = analyze_with_ollama(plate_img, model_choice)
                            
                            if isinstance(result, str):
                                st.markdown(f"**VLM Analiz Sonucu:**  \n```\n{result}\n```")
                                
                                if "APP" in str(result).upper():
                                    st.warning(f"🚗 **KARAR [Plaka #{idx+1}]: APP PLAKA** (Modifiye / Özel)")
                                elif "STANDARD" in str(result).upper() or "STANDART" in str(result).upper():
                                    st.info(f"📋 **KARAR [Plaka #{idx+1}]: STANDART PLAKA** (Resmi)")
                            else:
                                st.error(f"Hata: {result}")
                else:
                    st.warning(f"❗ Plaka #{idx+1} için hatalı koordinat sınırları (Geçildi).")
                
                st.markdown("---")

st.markdown("---")
st.caption("💬 Not: Ollama'nın ilk çalıştırması AMD GPU optimizasyonunu başlatır. İkinci ve sonraki çalıştırmalarda daha hızlı olacaktır.")
