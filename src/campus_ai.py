"""
campus_ai.py
Modules de démonstration pour EcoSmart Campus AI.

Ces fonctions rendent la plateforme utilisable sans entraîner de nouveaux modèles lourds.
Elles représentent les modules MLP, RNN/LSTM et Seq2Seq sous forme de prototypes
expliquables pour la démonstration.
"""

from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable

import numpy as np


@dataclass(frozen=True)
class EcoScoreInput:
    recycled_items: int
    electricity_kwh: float
    water_liters: float
    participation: int
    transport_score: int


FAQ = {
    "plastique": "Une bouteille ou un emballage plastique propre va dans la catégorie Plastique.",
    "carton": "Le carton propre et sec est recyclable. Il doit être aplati si possible.",
    "verre": "Les bouteilles et bocaux en verre vont dans la catégorie Verre.",
    "metal": "Les canettes et boîtes métalliques vont dans la catégorie Métal.",
    "métal": "Les canettes et boîtes métalliques vont dans la catégorie Métal.",
    "papier": "Le papier propre va dans la catégorie Papier. Le papier très sale doit être vérifié.",
    "trash": "Les déchets non recyclables vont dans la catégorie Déchet non recyclable.",
    "energie": "Pour réduire l'énergie, éteignez les lumières et les appareils inutilisés.",
    "énergie": "Pour réduire l'énergie, éteignez les lumières et les appareils inutilisés.",
    "score": "Le score écologique estime les habitudes de tri, consommation et participation.",
}


def predict_eco_score(inputs: EcoScoreInput) -> dict:
    """
    Prototype MLP : calcule un score écologique à partir de données tabulaires.

    Dans une version entraînée, ces variables seraient passées à un MLP Keras.
    Ici, on utilise une formule pondérée pour obtenir un résultat stable et
    compréhensible pendant la présentation.
    """
    recycling = min(inputs.recycled_items / 40, 1.0) * 35
    electricity = max(0.0, 1.0 - inputs.electricity_kwh / 250) * 25
    water = max(0.0, 1.0 - inputs.water_liters / 3500) * 15
    participation = min(inputs.participation / 10, 1.0) * 15
    transport = min(inputs.transport_score / 10, 1.0) * 10
    score = round(recycling + electricity + water + participation + transport, 1)

    if score >= 80:
        label = "Excellent"
    elif score >= 60:
        label = "Bon"
    elif score >= 40:
        label = "Moyen"
    else:
        label = "À améliorer"

    return {
        "score": score,
        "label": label,
        "details": {
            "Tri": round(recycling, 1),
            "Électricité": round(electricity, 1),
            "Eau": round(water, 1),
            "Participation": round(participation, 1),
            "Transport": round(transport, 1),
        },
    }


def forecast_energy(history: Iterable[float], days: int = 7) -> list[float]:
    """
    Prototype RNN/LSTM : prédit une série future à partir d'un historique.

    Une version avancée utiliserait un vrai LSTM entraîné. Pour la démonstration,
    on reproduit le comportement attendu : utiliser les valeurs précédentes pour
    estimer les prochains jours avec une tendance et une moyenne mobile.
    """
    values = np.array(list(history), dtype=float)
    if values.size < 3:
        raise ValueError("Il faut au moins 3 valeurs historiques.")

    forecasts = []
    current = values.copy()
    for _ in range(days):
        recent = current[-3:]
        trend = (recent[-1] - recent[0]) / 2
        next_value = max(0.0, float(recent.mean() + 0.35 * trend))
        forecasts.append(round(next_value, 2))
        current = np.append(current, next_value)
    return forecasts


def answer_question(question: str) -> dict:
    """
    Prototype Seq2Seq/FAQ : renvoie une réponse de chatbot.

    Une version Seq2Seq complète générerait la réponse mot par mot. Ici, on
    simule un assistant de tri fiable avec appariement de question.
    """
    normalized = question.lower().strip()
    if not normalized:
        return {
            "answer": "Posez une question sur le tri, l'énergie ou le score écologique.",
            "confidence": 0.0,
            "matched_topic": "aucun",
        }

    best_key = ""
    best_score = 0.0
    for key in FAQ:
        score = max(
            SequenceMatcher(None, normalized, key).ratio(),
            1.0 if key in normalized else 0.0,
        )
        if score > best_score:
            best_score = score
            best_key = key

    if best_score < 0.35:
        return {
            "answer": "Je n'ai pas assez d'information. Reformulez avec un mot comme plastique, carton, verre, énergie ou score.",
            "confidence": round(best_score, 2),
            "matched_topic": "inconnu",
        }

    return {
        "answer": FAQ[best_key],
        "confidence": round(best_score, 2),
        "matched_topic": best_key,
    }


def model_catalog() -> list[dict]:
    return [
        {
            "name": "MLP",
            "data": "Données tabulaires",
            "module": "Score écologique",
            "role": "Prédit un score à partir de variables numériques.",
        },
        {
            "name": "CNN / MobileNetV2",
            "data": "Images",
            "module": "Reconnaissance des déchets",
            "role": "Identifie la classe du déchet à partir d'une photo.",
        },
        {
            "name": "RNN / LSTM",
            "data": "Séries temporelles",
            "module": "Prévision énergie",
            "role": "Prévoit les consommations des prochains jours.",
        },
        {
            "name": "Seq2Seq",
            "data": "Texte / séquences",
            "module": "Assistant de tri",
            "role": "Répond aux questions de l'utilisateur.",
        },
    ]
