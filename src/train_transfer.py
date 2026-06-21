"""
train_transfer.py
Entraînement du modèle Transfer Learning (MobileNetV2).
"""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    BATCH_SIZE,
    CLASS_INDICES_PATH,
    DATA_DIR,
    EPOCHS,
    IMAGES_DIR,
    TRANSFER_EPOCHS,
    TRANSFER_IMG_SIZE,
    TRANSFER_MODEL_PATH,
    ensure_dirs,
)
from model_transfer import build_transfer_model
from preprocessing import create_transfer_generators


def train_transfer(epochs=TRANSFER_EPOCHS):
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"Dataset introuvable : {DATA_DIR}\n"
            "Téléchargez le dataset Kaggle et placez-le dans data/garbage/."
        )

    ensure_dirs()

    train_generator, val_generator = create_transfer_generators(
        str(DATA_DIR),
        img_size=TRANSFER_IMG_SIZE,
        batch_size=BATCH_SIZE,
    )

    num_classes = len(train_generator.class_indices)

    with open(CLASS_INDICES_PATH, "w", encoding="utf-8") as f:
        json.dump(train_generator.class_indices, f, indent=4)

    model = build_transfer_model(
        input_shape=(*TRANSFER_IMG_SIZE, 3),
        num_classes=num_classes,
        trainable_base=False,
    )

    early_stop = EarlyStopping(
        monitor="val_loss",
        patience=4,
        restore_best_weights=True,
    )
    reduce_lr = ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.3,
        patience=2,
        min_lr=1e-6,
    )

    print("Phase 1 : entraînement des couches supérieures (base gelée)...")
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        callbacks=[early_stop, reduce_lr],
    )

    print("Phase 2 : fine-tuning des dernières couches MobileNetV2...")
    for layer in model.layers:
        layer.trainable = False
    for layer in model.layers[-35:]:
        if not isinstance(layer, BatchNormalization):
            layer.trainable = True

    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    history_fine = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=5,
        callbacks=[early_stop, reduce_lr],
    )

    val_loss, val_accuracy = model.evaluate(val_generator)
    print(f"Validation Accuracy (Transfer) : {val_accuracy:.4f}")

    predictions = model.predict(val_generator)
    y_pred = predictions.argmax(axis=1)
    y_true = val_generator.classes
    class_names = list(train_generator.class_indices.keys())

    print("Matrice de confusion :")
    print(confusion_matrix(y_true, y_pred))

    print("Classification report :")
    print(classification_report(y_true, y_pred, target_names=class_names))

    for key in ("accuracy", "val_accuracy", "loss", "val_loss"):
        history.history[key].extend(history_fine.history[key])

    plt.figure()
    plt.plot(history.history["accuracy"], label="Train Accuracy")
    plt.plot(history.history["val_accuracy"], label="Validation Accuracy")
    plt.legend()
    plt.title("Courbe Accuracy (Transfer Learning)")
    plt.savefig(IMAGES_DIR / "transfer_accuracy_curve.png")

    plt.figure()
    plt.plot(history.history["loss"], label="Train Loss")
    plt.plot(history.history["val_loss"], label="Validation Loss")
    plt.legend()
    plt.title("Courbe Loss (Transfer Learning)")
    plt.savefig(IMAGES_DIR / "transfer_loss_curve.png")

    model.save(TRANSFER_MODEL_PATH)
    print(f"Modèle sauvegardé dans {TRANSFER_MODEL_PATH}")


if __name__ == "__main__":
    train_transfer()
