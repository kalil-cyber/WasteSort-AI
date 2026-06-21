"""
inference.py
Fonctions d'inférence partagées (CLI, Streamlit, webcam).
"""

import json
from io import BytesIO
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image, ImageEnhance, ImageOps
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image

from config import CLASS_INDICES_PATH, CLASS_LABELS_FR, MODEL_PATH, TRANSFER_MODEL_PATH


def load_model_and_classes(model_path=None):
    if model_path is None and TRANSFER_MODEL_PATH.exists():
        model_path = TRANSFER_MODEL_PATH
    elif model_path is None:
        model_path = MODEL_PATH
    model_path = Path(model_path)
    class_indices_path = CLASS_INDICES_PATH

    if not model_path.exists():
        raise FileNotFoundError(
            "Aucun modèle trouvé. Lancez python src/train.py ou python src/train_transfer.py"
        )

    model = tf.keras.models.load_model(model_path)

    with open(class_indices_path, "r", encoding="utf-8") as f:
        class_indices = json.load(f)

    index_to_class = {v: k for k, v in class_indices.items()}
    return model, index_to_class


def get_model_input_size(model):
    input_shape = model.input_shape
    if isinstance(input_shape, list):
        input_shape = input_shape[0]
    return int(input_shape[1]), int(input_shape[2])


def is_transfer_model(model):
    return get_model_input_size(model) == (224, 224) or any(
        "mobilenet" in layer.name.lower() for layer in model.layers
    )


def preprocess_pil(img: Image.Image, target_size=(150, 150), transfer_model=False):
    img = img.convert("RGB").resize(target_size)
    img_array = keras_image.img_to_array(img)
    if transfer_model:
        img_array = preprocess_input(img_array)
    else:
        img_array = img_array / 255.0
    return np.expand_dims(img_array, axis=0)


def prediction_variants(img: Image.Image):
    """
    Crée quelques variantes légères pour rendre la prédiction plus stable.

    On évite les transformations fortes : le but est de simuler de petites différences
    de cadrage et de lumière sans changer la nature de l'objet.
    """
    img = img.convert("RGB")
    return [
        img,
        ImageOps.mirror(img),
        img.rotate(5, resample=Image.Resampling.BILINEAR, expand=False),
        img.rotate(-5, resample=Image.Resampling.BILINEAR, expand=False),
        ImageEnhance.Brightness(img).enhance(0.9),
        ImageEnhance.Brightness(img).enhance(1.1),
        ImageEnhance.Contrast(img).enhance(1.1),
    ]


def predict_from_pil(
    img: Image.Image,
    model=None,
    index_to_class=None,
    model_path=None,
    use_tta=True,
):
    if model is None or index_to_class is None:
        model, index_to_class = load_model_and_classes(model_path)

    target_size = get_model_input_size(model)
    variants = prediction_variants(img) if use_tta else [img]
    batch = np.vstack(
        [
            preprocess_pil(
                variant,
                target_size=target_size,
                transfer_model=is_transfer_model(model),
            )
            for variant in variants
        ]
    )

    predictions_batch = model.predict(batch, verbose=0)
    predictions = predictions_batch.mean(axis=0)
    predicted_index = int(np.argmax(predictions))
    predicted_class = index_to_class[predicted_index]
    confidence = float(predictions[predicted_index])
    sorted_predictions = np.sort(predictions)[::-1]
    margin = float(sorted_predictions[0] - sorted_predictions[1]) if len(sorted_predictions) > 1 else confidence

    probabilities = {
        CLASS_LABELS_FR.get(index_to_class[i], index_to_class[i]): float(predictions[i])
        for i in range(len(predictions))
    }

    return {
        "class": predicted_class,
        "label_fr": CLASS_LABELS_FR.get(predicted_class, predicted_class),
        "confidence": confidence,
        "margin": margin,
        "probabilities": probabilities,
    }


def predict_from_bytes(image_bytes: bytes, model_path=None):
    img = Image.open(BytesIO(image_bytes))
    return predict_from_pil(img, model_path=model_path)
