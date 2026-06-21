"""
webcam_predict.py
Classification en temps réel via webcam (OpenCV).
"""

import argparse
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import CLASS_LABELS_FR
from inference import get_model_input_size, is_transfer_model, load_model_and_classes, preprocess_pil
from PIL import Image
import numpy as np


def run_webcam(model_path=None, camera_index=0):
    model, index_to_class = load_model_and_classes(model_path)
    target_size = get_model_input_size(model)
    transfer_model = is_transfer_model(model)
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError("Impossible d'ouvrir la webcam.")

    print("Appuyez sur 'q' pour quitter.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_frame)
        img_array = preprocess_pil(
            pil_img,
            target_size=target_size,
            transfer_model=transfer_model,
        )

        predictions = model.predict(img_array, verbose=0)[0]
        predicted_index = int(np.argmax(predictions))
        predicted_class = index_to_class[predicted_index]
        confidence = float(predictions[predicted_index])
        label_fr = CLASS_LABELS_FR.get(predicted_class, predicted_class)

        text = f"{label_fr} ({confidence:.0%})"
        cv2.putText(
            frame,
            text,
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 200, 0),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("WasteSort AI - Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None, help="Chemin vers le modèle .keras")
    parser.add_argument("--camera", type=int, default=0, help="Index de la webcam")
    args = parser.parse_args()

    run_webcam(model_path=args.model, camera_index=args.camera)
