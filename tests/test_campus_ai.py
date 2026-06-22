"""Tests pour les modules EcoSmart Campus AI."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from campus_ai import EcoScoreInput, answer_question, forecast_energy, model_catalog, predict_eco_score


def test_eco_score_range():
    result = predict_eco_score(
        EcoScoreInput(
            recycled_items=30,
            electricity_kwh=120,
            water_liters=1800,
            participation=7,
            transport_score=8,
        )
    )
    assert 0 <= result["score"] <= 100
    assert result["label"] in {"Excellent", "Bon", "Moyen", "À améliorer"}


def test_energy_forecast_length():
    forecast = forecast_energy([120, 128, 125, 132, 140], days=5)
    assert len(forecast) == 5
    assert all(value >= 0 for value in forecast)


def test_energy_forecast_requires_history():
    with pytest.raises(ValueError):
        forecast_energy([120, 128], days=3)


def test_chatbot_answer_plastic():
    result = answer_question("Où jeter une bouteille plastique ?")
    assert "Plastique" in result["answer"]
    assert result["confidence"] > 0


def test_model_catalog_contains_core_models():
    names = {item["name"] for item in model_catalog()}
    assert {"MLP", "CNN / MobileNetV2", "RNN / LSTM", "Seq2Seq"}.issubset(names)
