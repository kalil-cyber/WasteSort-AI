"""
preprocessing.py
Préparation des images pour WasteSort AI.
"""

import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from config import SEED


def set_seed(seed=SEED):
    """Fixe les graines aléatoires pour la reproductibilité."""
    tf.random.set_seed(seed)


def create_generators(data_dir, img_size=(150, 150), batch_size=32, validation_split=0.2):
    """
    Crée les générateurs train et validation à partir d'un dossier contenant les classes.

    Exemple de structure :
    data/garbage/cardboard
    data/garbage/glass
    data/garbage/metal
    data/garbage/paper
    data/garbage/plastic
    data/garbage/trash
    """
    set_seed()

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        validation_split=validation_split,
        rotation_range=20,
        zoom_range=0.2,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True,
    )

    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
        seed=SEED,
    )

    val_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
        seed=SEED,
        shuffle=False,
    )

    return train_generator, val_generator


def create_transfer_generators(data_dir, img_size=(224, 224), batch_size=32, validation_split=0.2):
    """
    Crée les générateurs adaptés à MobileNetV2.

    MobileNetV2 attend des pixels prétraités avec preprocess_input, pas une simple
    division par 255. C'est important pour obtenir de bonnes prédictions réelles.
    """
    set_seed()

    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=validation_split,
        rotation_range=25,
        zoom_range=0.25,
        width_shift_range=0.12,
        height_shift_range=0.12,
        shear_range=0.12,
        brightness_range=(0.8, 1.2),
        horizontal_flip=True,
        fill_mode="nearest",
    )

    val_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=validation_split,
    )

    train_generator = train_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="training",
        seed=SEED,
    )

    val_generator = val_datagen.flow_from_directory(
        data_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset="validation",
        seed=SEED,
        shuffle=False,
    )

    return train_generator, val_generator
