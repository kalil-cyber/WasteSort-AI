"""
config.py
Chemins et constantes centralisés pour WasteSort AI.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data" / "garbage"
MODELS_DIR = PROJECT_ROOT / "models"
IMAGES_DIR = PROJECT_ROOT / "images"

MODEL_PATH = MODELS_DIR / "wastesort_model.keras"
TRANSFER_MODEL_PATH = MODELS_DIR / "wastesort_transfer_model.keras"
CLASS_INDICES_PATH = MODELS_DIR / "class_indices.json"

IMG_SIZE = (150, 150)
TRANSFER_IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15
TRANSFER_EPOCHS = 10
SEED = 42

CLASS_LABELS_FR = {
    "cardboard": "Carton",
    "glass": "Verre",
    "metal": "Métal",
    "paper": "Papier",
    "plastic": "Plastique",
    "trash": "Déchet non recyclable",
}


def ensure_dirs():
    """Crée les dossiers de sortie s'ils n'existent pas."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
