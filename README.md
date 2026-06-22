# EcoSmart Campus AI

Plateforme IA multi-modèles pour un campus durable.

Le projet étend WasteSort AI en une application complète qui regroupe plusieurs familles de modèles :

- **CNN / MobileNetV2** pour reconnaître les déchets à partir d'une image ;
- **MLP** pour calculer un score écologique à partir de données tabulaires ;
- **RNN / LSTM** pour prévoir une consommation d'énergie ;
- **Seq2Seq / FAQ** pour répondre aux questions des utilisateurs ;
- **Streamlit** pour regrouper tous les modules dans une interface web.

## Objectif

L'objectif est de montrer comment plusieurs modèles d'intelligence artificielle peuvent être utilisés dans une même plateforme.

EcoSmart Campus AI permet de :

- classifier un déchet par image ;
- calculer un score écologique ;
- prévoir une consommation énergétique ;
- répondre aux questions de tri ;
- comparer les modèles MLP, CNN, RNN/LSTM, Seq2Seq et MobileNetV2.

## Lancement

```bash
streamlit run app/streamlit_app.py
```

Puis ouvrir :

```text
http://localhost:8501
```

## Modules

### 1. Déchets - CNN / MobileNetV2

Ce module reprend WasteSort AI. L'utilisateur envoie une image et le modèle prédit une catégorie :

- carton ;
- verre ;
- métal ;
- papier ;
- plastique ;
- déchet non recyclable.

Le modèle utilisé par défaut est MobileNetV2 avec Transfer Learning.

### 2. Score écologique - MLP

Ce module illustre un MLP appliqué à des données tabulaires.

Entrées :

- nombre de déchets triés ;
- consommation électrique ;
- consommation d'eau ;
- participation aux actions écologiques ;
- transport durable.

Sortie :

- score écologique sur 100 ;
- label : Excellent, Bon, Moyen, À améliorer.

### 3. Prévision énergie - RNN / LSTM

Ce module utilise un historique de consommation pour prévoir les prochains jours.

Une version complète utiliserait un LSTM entraîné sur une série temporelle. La version actuelle est un prototype explicable qui reproduit la logique de prévision.

### 4. Assistant tri - Seq2Seq / FAQ

Ce module répond aux questions des utilisateurs sur le tri et l'énergie.

Une version avancée utiliserait un modèle Seq2Seq entraîné. La version actuelle utilise une base FAQ fiable pour la démonstration.

## Technologies

- Python
- TensorFlow / Keras
- MobileNetV2
- Streamlit
- NumPy
- Scikit-learn
- Pillow
- Matplotlib

## Structure

```text
EcoSmart-Campus-AI/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── garbage/
│   ├── eco_scores.csv
│   ├── energy_consumption.csv
│   └── chatbot_faq.csv
├── src/
│   ├── campus_ai.py
│   ├── inference.py
│   ├── model.py
│   ├── model_transfer.py
│   ├── train.py
│   └── train_transfer.py
├── assets/
├── exports/
├── tests/
└── README.md
```

## Résultat

La plateforme montre plusieurs types d'IA dans un seul projet :

| Modèle | Type de données | Module |
| --- | --- | --- |
| MLP | Données tabulaires | Score écologique |
| CNN / MobileNetV2 | Images | Reconnaissance des déchets |
| RNN / LSTM | Séries temporelles | Prévision énergie |
| Seq2Seq | Texte / séquences | Assistant de tri |

## Limites

Les modules MLP, LSTM et Seq2Seq sont des prototypes de démonstration. Ils montrent la logique de chaque modèle, mais ils peuvent être remplacés plus tard par des modèles entraînés sur de vrais datasets.

La partie image reste le module le plus avancé du projet grâce au modèle MobileNetV2 entraîné sur le dataset Garbage Classification.
