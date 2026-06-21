"""
download_dataset.py
Télécharge et organise le dataset Kaggle « Garbage Classification ».

Prérequis :
  1. Créer un compte Kaggle : https://www.kaggle.com
  2. Télécharger votre token API (Settings > API > Create New Token)
  3. Placer kaggle.json dans :
     - Windows : C:\\Users\\<vous>\\.kaggle\\kaggle.json
     - Linux/Mac : ~/.kaggle/kaggle.json
  4. pip install kaggle
"""

import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "garbage"
TEMP_DIR = PROJECT_ROOT / "data" / "_kaggle_tmp"

DATASET = "asdasdasasdas/garbage-classification"
CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]


def check_kaggle():
    try:
        subprocess.run(
            ["kaggle", "--version"],
            check=True,
            capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def organize_dataset(source_dir: Path):
    """Réorganise le dataset Kaggle dans data/garbage/."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for cls in CLASSES:
        (DATA_DIR / cls).mkdir(exist_ok=True)

    # Le dataset Kaggle a souvent une structure Garbage classification/Garbage classification/
    candidates = list(source_dir.rglob("*"))
    image_ext = {".jpg", ".jpeg", ".png", ".bmp"}

    moved = 0
    for path in candidates:
        if path.suffix.lower() not in image_ext:
            continue
        parent_name = path.parent.name.lower()
        for cls in CLASSES:
            if cls in parent_name or parent_name == cls:
                dest = DATA_DIR / cls / path.name
                if not dest.exists():
                    shutil.copy2(path, dest)
                    moved += 1
                break

    return moved


def main():
    if DATA_DIR.exists() and any(DATA_DIR.iterdir()):
        count = sum(1 for cls in CLASSES if (DATA_DIR / cls).exists() for _ in (DATA_DIR / cls).iterdir())
        if count > 0:
            print(f"Dataset déjà présent ({count} images dans {DATA_DIR})")
            return

    if not check_kaggle():
        print("Kaggle CLI non installé ou non configuré.")
        print()
        print("Installation manuelle :")
        print(f"  1. Téléchargez : https://www.kaggle.com/datasets/{DATASET}")
        print(f"  2. Extrayez les images dans {DATA_DIR}/")
        print("     avec les sous-dossiers : cardboard, glass, metal, paper, plastic, trash")
        sys.exit(1)

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Téléchargement de {DATASET}...")
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", DATASET, "-p", str(TEMP_DIR), "--unzip"],
        check=True,
    )

    moved = organize_dataset(TEMP_DIR)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)

    print(f"Dataset organisé : {moved} images copiées dans {DATA_DIR}")
    print("Lancez maintenant : python src/train.py")


if __name__ == "__main__":
    main()
