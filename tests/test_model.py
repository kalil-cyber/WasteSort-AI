"""Tests unitaires pour WasteSort AI."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from model import build_cnn_model
from model_transfer import build_transfer_model
from config import IMG_SIZE, CLASS_LABELS_FR


class TestModel:
    def test_cnn_output_shape(self):
        model = build_cnn_model(input_shape=(*IMG_SIZE, 3), num_classes=6)
        assert model.output_shape == (None, 6)

    def test_cnn_compiled(self):
        model = build_cnn_model(num_classes=6)
        assert model.optimizer is not None
        metric_names = [m.name for m in model.metrics]
        assert metric_names  # accuracy ou compile_metrics selon la version Keras

    def test_transfer_model_output_shape(self):
        model = build_transfer_model(input_shape=(*IMG_SIZE, 3), num_classes=6)
        assert model.output_shape == (None, 6)


class TestConfig:
    def test_class_labels_count(self):
        assert len(CLASS_LABELS_FR) == 6

    def test_class_labels_keys(self):
        expected = {"cardboard", "glass", "metal", "paper", "plastic", "trash"}
        assert set(CLASS_LABELS_FR.keys()) == expected


class TestInference:
    def test_predict_from_pil_without_model(self):
        from PIL import Image
        import inference

        img = Image.new("RGB", IMG_SIZE, color=(128, 128, 128))

        with pytest.raises(FileNotFoundError):
            inference.predict_from_pil(img, model_path=ROOT / "models" / "missing_model.keras")
