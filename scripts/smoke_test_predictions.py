"""
smoke_test_predictions.py
Teste rapidement le modèle entraîné sur une image par classe.
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from inference import load_model_and_classes, predict_from_pil  # noqa: E402


def main():
    model_path = ROOT / "models" / "wastesort_transfer_model.keras"
    data_dir = ROOT / "data" / "garbage"

    model, classes = load_model_and_classes(model_path)

    for folder in sorted(data_dir.iterdir()):
        if not folder.is_dir():
            continue

        image_path = next(folder.glob("*.jpg"), None)
        if image_path is None:
            continue

        result = predict_from_pil(Image.open(image_path), model, classes)
        print(
            f"{folder.name}: {image_path.name} -> "
            f"{result['class']} ({result['label_fr']}) "
            f"{result['confidence']:.2%}"
        )


if __name__ == "__main__":
    main()
