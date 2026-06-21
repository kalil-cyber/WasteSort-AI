# WasteSort AI - Plateforme Deep Learning

Plateforme web de classification automatique des déchets recyclables avec Deep Learning.

Le projet est pensé pour une présentation publique, un portfolio étudiant, un CV
ou une démonstration école. L'interface Streamlit permet d'envoyer une photo,
d'obtenir une prédiction et d'expliquer simplement le résultat au public.

## Objectif

Créer un modèle CNN capable de classifier une image de déchet en 6 catégories :

| Classe | Label FR |
|--------|----------|
| cardboard | Carton |
| glass | Verre |
| metal | Métal |
| paper | Papier |
| plastic | Plastique |
| trash | Déchet non recyclable |

Projet conçu pour un **portfolio étudiant**, un CV, une présentation école ou une candidature en entreprise.

## Démonstration publique

```bash
streamlit run app/streamlit_app.py
```

La plateforme contient :

- une page de démonstration simple pour le public ;
- un upload image et une prise de photo via caméra ;
- une prédiction avec confiance et probabilités par classe ;
- un statut `Fiable`, `À vérifier` ou `Incertain` ;
- une explication pédagogique du modèle MobileNetV2 ;
- une explication claire du fonctionnement.

## Structure du projet

```text
WasteSort-AI/
├── app/
│   └── streamlit_app.py      # Plateforme web de présentation
├── data/
│   └── garbage/              # Dataset (à télécharger)
├── images/                   # Courbes d'entraînement
├── models/                   # Modèles entraînés
├── notebook/
│   └── wastesort_ai.ipynb    # Version Google Colab
├── scripts/
│   └── download_dataset.py   # Téléchargement Kaggle
│   └── smoke_test_predictions.py
├── src/
│   ├── config.py             # Configuration centralisée
│   ├── preprocessing.py      # Data augmentation
│   ├── model.py              # CNN simple
│   ├── model_transfer.py     # MobileNetV2
│   ├── train.py              # Entraînement CNN
│   ├── train_transfer.py     # Entraînement Transfer Learning
│   ├── predict.py            # Inférence CLI
│   ├── inference.py          # Inférence partagée
│   └── webcam_predict.py     # Webcam temps réel
├── tests/
│   └── test_model.py         # Tests unitaires
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Dataset

Dataset recommandé : [Garbage Classification (Kaggle)](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)

**Téléchargement automatique** (nécessite l'API Kaggle configurée) :

```bash
pip install kaggle
python scripts/download_dataset.py
```

**Téléchargement manuel** : extrayez les images dans `data/garbage/` avec les sous-dossiers `cardboard`, `glass`, `metal`, `paper`, `plastic`, `trash`.

## Entraînement

**CNN simple :**

```bash
python src/train.py
```

**Transfer Learning (MobileNetV2, recommandé) :**

```bash
python src/train_transfer.py
```

Les modèles et courbes sont sauvegardés dans `models/` et `images/`.

## Prédiction

**Ligne de commande :**

```bash
python src/predict.py --image chemin/vers/image.jpg
python src/predict.py --image chemin/vers/image.jpg --no-show --save resultat.png
```

**Application Streamlit :**

```bash
streamlit run app/streamlit_app.py
```

Le modèle utilisé par défaut est `MobileNetV2 (Transfer Learning)`, plus fiable
pour les photos réelles que le CNN simple.

**Webcam temps réel (OpenCV) :**

```bash
python src/webcam_predict.py
```

Appuyez sur `q` pour quitter.

## Tests

```bash
pip install pytest
pytest tests/ -v
```

Smoke test sur une image par classe :

```bash
python scripts/smoke_test_predictions.py
```

## Technologies

- Python 3.9+
- TensorFlow / Keras
- MobileNetV2
- Streamlit
- OpenCV
- Scikit-learn
- Matplotlib

## Ligne CV

**FR :** Développement d'un modèle CNN et Transfer Learning (MobileNetV2) avec TensorFlow/Keras pour classifier automatiquement des déchets recyclables, incluant une application Streamlit, une webcam temps réel, data augmentation et évaluation multi-classes.

**EN :** Built CNN and Transfer Learning (MobileNetV2) models with TensorFlow/Keras to classify recyclable waste images, including a Streamlit web app, real-time webcam inference, data augmentation and multi-class evaluation.

## Perspectives

- [x] Transfer Learning MobileNetV2
- [x] Application Streamlit
- [x] Webcam temps réel OpenCV
- [ ] Fine-tuning EfficientNet
