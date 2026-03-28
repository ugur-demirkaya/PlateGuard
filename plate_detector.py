import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from PIL import Image

@dataclass
class CroppedPlate:
    """Tespit edilen ve kırpılan plaka bilgisi."""
    image: np.ndarray          # Kırpılmış plaka görseli (BGR)
    image_pil: Image.Image     # Kırpılmış plaka görseli (PIL)
    bbox: tuple                # (x1, y1, x2, y2)
    confidence: float          # Tespit güven skoru
    class_name: str = ""       # Algılanan sınıf adı

class PlateDetector:
    """YOLO tabanlı plaka tespit motoru."""

    # HuggingFace'den plaka-spesifik model
    HF_MODEL_REPO = "morsetechlab/yolov11-license-plate-detection"
    HF_MODEL_FILE = "license-plate-finetune-v1n.pt"
    LOCAL_MODEL_NAME = "yolov11n-plate-detect.pt"

    def __init__(self, model_path: Optional[str] = None):
        """
        Args:
            model_path: YOLO model dosyası yolu. None ise HuggingFace'den
                        plaka-spesifik model indirilir.
        """
        from ultralytics import YOLO

        if model_path and os.path.exists(model_path):
            self.model = YOLO(model_path)
        else:
            # Plaka-spesifik modeli yükle veya indir
            model_file = self._get_plate_model()
            self.model = YOLO(model_file)

        self._plate_classes = None

    def _get_plate_model(self) -> str:
        """
        Plaka tespit modeli dosya yolunu döner.
        Yoksa HuggingFace'den indirir.
        """
        models_dir = Path(__file__).parent / "models"
        models_dir.mkdir(exist_ok=True)
        local_path = models_dir / self.LOCAL_MODEL_NAME

        # Zaten indirilmiş mi?
        if local_path.exists():
            print(f"✅ Plaka modeli mevcut: {local_path}")
            return str(local_path)

        # HuggingFace'den indir
        print(f"⏳ Plaka tespit modeli indiriliyor: {self.HF_MODEL_REPO}...")
        try:
            from huggingface_hub import hf_hub_download

            downloaded = hf_hub_download(
                repo_id=self.HF_MODEL_REPO,
                filename=self.HF_MODEL_FILE,
                local_dir=str(models_dir),
            )
            # İndirilen dosyayı bilinen isme kopyala
            import shutil
            shutil.copy2(downloaded, str(local_path))
            print(f"✅ Plaka modeli indirildi: {local_path}")
            return str(local_path)

        except Exception as e:
            print(f"⚠️ HuggingFace indirme hatası: {e}")
            print("   Alternatif olarak genel YOLO modeli deneniyor...")
            # Fallback: genel model (plaka bulamaz ama çökmez)
            return "yolov8n.pt" # Fallback to standard yolo if hf fails

    def detect_plates(
        self,
        image_source,
        confidence_threshold: float = 0.25,
        target_classes: Optional[List[str]] = None,
    ) -> List[CroppedPlate]:
        """
        Görüntüdeki plaka alanlarını tespit eder ve kırpar.
        """
        # Görüntüyü yükle
        if isinstance(image_source, str) or isinstance(image_source, Path):
            image = cv2.imread(str(image_source))
            if image is None:
                raise ValueError(f"Görüntü okunamadı: {image_source}")
        elif isinstance(image_source, Image.Image):
            image = cv2.cvtColor(np.array(image_source), cv2.COLOR_RGB2BGR)
        elif isinstance(image_source, np.ndarray):
            image = image_source.copy()
        else:
            raise TypeError(f"Desteklenmeyen görüntü tipi: {type(image_source)}")

        # YOLO çıkarım
        results = self.model(image, conf=confidence_threshold, verbose=False)

        cropped_plates = []

        for result in results:
            if result.boxes is None or len(result.boxes) == 0:
                continue

            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0])
                cls_id = int(box.cls[0])
                cls_name = result.names.get(cls_id, str(cls_id))

                # Sınıf filtresi
                if target_classes and cls_name not in target_classes:
                    continue

                # Sınır kontrolü
                h, w = image.shape[:2]
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w, x2)
                y2 = min(h, y2)

                # Kırp
                cropped = image[y1:y2, x1:x2]
                if cropped.size == 0:
                    continue

                # PIL dönüşümü
                cropped_rgb = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cropped_rgb)

                cropped_plates.append(CroppedPlate(
                    image=cropped,
                    image_pil=pil_image,
                    bbox=(x1, y1, x2, y2),
                    confidence=conf,
                    class_name=cls_name,
                ))

        # Güven skoruna göre sırala
        cropped_plates.sort(key=lambda p: p.confidence, reverse=True)
        return cropped_plates

def crop_plate_region(image: np.ndarray, bbox: tuple, padding: int = 10) -> np.ndarray:
    """Verilen bbox etrafında padding ile plaka bölgesini kırpar."""
    h, w = image.shape[:2]
    x1, y1, x2, y2 = bbox

    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(w, x2 + padding)
    y2 = min(h, y2 + padding)

    return image[y1:y2, x1:x2]
