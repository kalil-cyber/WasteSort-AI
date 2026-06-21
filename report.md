# Rapport Professionnel — WasteSort AI

## 1. Introduction
La gestion des déchets constitue un enjeu majeur pour les villes modernes. Le tri manuel des déchets peut être lent, coûteux et parfois imprécis. L’intelligence artificielle offre une solution intéressante pour automatiser la reconnaissance des déchets à partir d’images.

Le projet WasteSort AI vise à développer un modèle de Deep Learning capable de classifier automatiquement des déchets recyclables selon plusieurs catégories : plastic, paper, glass, metal, cardboard et trash.

## 2. Problématique
Comment utiliser le Deep Learning pour reconnaître automatiquement le type de déchet à partir d’une image et faciliter le tri sélectif ?

## 3. Objectif
L’objectif principal est de construire un modèle CNN avec TensorFlow/Keras capable de classifier les images de déchets en plusieurs classes.

## 4. Dataset
Le dataset recommandé est Garbage Classification disponible sur Kaggle. Il contient plusieurs dossiers correspondant aux classes de déchets.

Structure attendue :

- cardboard
- glass
- metal
- paper
- plastic
- trash

## 5. Prétraitement
Les images sont redimensionnées en 150x150 pixels puis normalisées entre 0 et 1. Une data augmentation est appliquée pour améliorer la généralisation du modèle.

Les transformations utilisées sont :

- rotation
- zoom
- déplacement horizontal
- déplacement vertical
- retournement horizontal

## 6. Architecture CNN
Le modèle CNN contient :

- Conv2D
- MaxPooling2D
- Flatten
- Dense
- Dropout
- Softmax

La couche Softmax permet d’obtenir une probabilité pour chaque classe.

## 7. Entraînement
Le modèle est compilé avec :

- Optimizer : Adam
- Loss : categorical_crossentropy
- Métrique : accuracy

Un EarlyStopping est utilisé afin de limiter le surapprentissage.

## 8. Évaluation
L’évaluation repose sur :

- Accuracy
- Precision
- Recall
- F1-score
- Matrice de confusion
- Classification report

## 9. Résultats
Le modèle permet de reconnaître automatiquement plusieurs catégories de déchets. Les résultats peuvent varier selon la qualité du dataset et le nombre d’images disponibles par classe.

## 10. Limites
Le modèle peut rencontrer des difficultés lorsque :

- l’image est floue ;
- l’objet est partiellement visible ;
- le fond est trop complexe ;
- certaines classes se ressemblent.

## 11. Perspectives
Les améliorations possibles sont :

- utiliser MobileNetV2 ou EfficientNet ;
- créer une application Streamlit ;
- ajouter une caméra en temps réel ;
- déployer le modèle sur le Web ;
- utiliser un dataset plus large.

## 12. Conclusion
WasteSort AI est un projet complet de Deep Learning appliqué à un problème concret : le tri automatique des déchets. Il est simple à comprendre, utile, visuel et valorisant pour un portfolio Data Science / IA.
