"""
predict.py
Tester WasteSort AI sur une nouvelle image.
"""

import argparse
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import CLASS_INDICES_PATH, MODEL_PATH, TRANSFER_MODEL_PATH
from inference import load_model_and_classes, predict_from_pil


def predict_image(model_path, image_path, class_indices_path, show=True, save_path=None):
    model_path = Path(model_path)
    image_path = Path(image_path)
    class_indices_path = Path(class_indices_path)

    if not model_path.exists():
        raise FileNotFoundError(
            f"Modèle introuvable : {model_path}\n"
            "Lancez d'abord : python src/train.py"
        )
    if not image_path.exists():
        raise FileNotFoundError(f"Image introuvable : {image_path}")
    if not class_indices_path.exists():
        raise FileNotFoundError(f"Indices de classes introuvables : {class_indices_path}")

    model, index_to_class = load_model_and_classes(model_path)
    img = Image.open(image_path)
    result = predict_from_pil(img, model, index_to_class)

    print(f"Classe prédite : {result['class']} ({result['label_fr']})")
    print(f"Confiance : {result['confidence']:.2%}")

    if show or save_path:
        plt.imshow(img)
        plt.title(f"{result['label_fr']} — Confiance : {result['confidence']:.2%}")
        plt.axis("off")
        if save_path:
            plt.savefig(save_path, bbox_inches="tight")
            print(f"Résultat sauvegardé : {save_path}")
        if show:
            plt.show()
        else:
            plt.close()

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Chemin vers l'image à tester")
    default_model = TRANSFER_MODEL_PATH if TRANSFER_MODEL_PATH.exists() else MODEL_PATH
    parser.add_argument("--model", default=str(default_model))
    parser.add_argument("--classes", default=str(CLASS_INDICES_PATH))
    parser.add_argument("--save", default=None, help="Sauvegarder le résultat en image")
    parser.add_argument("--no-show", action="store_true", help="Ne pas afficher la fenêtre")
    args = parser.parse_args()

    predict_image(
        args.model,
        args.image,
        args.classes,
        show=not args.no_show,
        save_path=args.save,
    )
