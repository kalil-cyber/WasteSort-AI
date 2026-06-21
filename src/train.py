"""
train.py
Entraînement du modèle WasteSort AI.
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.callbacks import EarlyStopping

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    BATCH_SIZE,
    CLASS_INDICES_PATH,
    DATA_DIR,
    EPOCHS,
    IMAGES_DIR,
    IMG_SIZE,
    MODEL_PATH,
    ensure_dirs,
)
from model import build_cnn_model
from preprocessing import create_generators


def train():
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {DATA_DIR}\n"
            "Téléchargez le dataset Kaggle « Garbage Classification » "
            "et placez-le dans data/garbage/ (voir scripts/download_dataset.py)."
        )

    ensure_dirs()

    train_generator, val_generator = create_generators(
        str(DATA_DIR),
        img_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
    )

    num_classes = len(train_generator.class_indices)

    with open(CLASS_INDICES_PATH, "w", encoding="utf-8") as f:
        json.dump(train_generator.class_indices, f, indent=4)

    model = build_cnn_model(input_shape=(*IMG_SIZE, 3), num_classes=num_classes)

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
    )

    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=EPOCHS,
        callbacks=[early_stop],
    )

    val_loss, val_accuracy = model.evaluate(val_generator)
    print(f"Validation Accuracy : {val_accuracy:.4f}")

    predictions = model.predict(val_generator)
    y_pred = predictions.argmax(axis=1)
    y_true = val_generator.classes
    class_names = list(train_generator.class_indices.keys())

    print("Matrice de confusion :")
    print(confusion_matrix(y_true, y_pred))

    print("Classification report :")
    print(classification_report(y_true, y_pred, target_names=class_names))

    plt.figure()
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
    plt.legend()
    plt.title("Courbe Accuracy")
    plt.savefig(IMAGES_DIR / "accuracy_curve.png")

    plt.figure()
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.legend()
    plt.title("Courbe Loss")
    plt.savefig(IMAGES_DIR / "loss_curve.png")

    model.save(MODEL_PATH)
    print(f"Modèle sauvegardé dans {MODEL_PATH}")


if __name__ == "__main__":
    train()
