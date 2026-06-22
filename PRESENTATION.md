# Présentation Complète - WasteSort AI

## Informations De Présentation

**Titre du projet :** WasteSort AI  
**Nom de l'étudiant :** ......  
**Nom de la prof :** ......  
**Classe / formation :** ......  
**Établissement :** ......  
**Année scolaire :** ......  
**Sujet :** Reconnaissance automatique des déchets avec Deep Learning

**Logo école :** EMSI

## 1. Plan De Présentation Orale 5 À 7 Minutes

### 1. Introduction

Bonjour, aujourd'hui je vais vous présenter mon projet **WasteSort AI**.

WasteSort AI est une application web qui utilise l'intelligence artificielle pour reconnaître automatiquement le type de déchet à partir d'une photo.

### 2. Problématique

Le tri des déchets est important pour le recyclage, mais il n'est pas toujours facile de savoir dans quelle catégorie placer un objet.

Par exemple, certains emballages peuvent ressembler à du papier ou à du plastique, et certains déchets non recyclables peuvent être confondus avec des matériaux recyclables.

### 3. Objectif Du Projet

L'objectif du projet est de créer une application simple qui aide l'utilisateur à identifier un déchet à partir d'une image.

Le système reconnaît six catégories :

- carton ;
- verre ;
- métal ;
- papier ;
- plastique ;
- déchet non recyclable.

### 4. Technologies Utilisées

Pour réaliser ce projet, j'ai utilisé plusieurs technologies :

- Python pour le développement ;
- TensorFlow et Keras pour le modèle de Deep Learning ;
- MobileNetV2 avec le Transfer Learning ;
- Streamlit pour créer l'interface web ;
- Scikit-learn et Matplotlib pour l'évaluation ;
- Pillow pour le traitement des images ;
- le dataset Garbage Classification disponible sur Kaggle.

### 5. Méthode

Au départ, j'ai testé un modèle CNN simple. Ce modèle fonctionnait, mais sa fiabilité était limitée sur des photos réelles.

J'ai donc utilisé MobileNetV2, un modèle déjà entraîné sur un grand nombre d'images. Grâce au Transfer Learning, j'ai adapté ce modèle à la classification des déchets.

### 6. Interface Web

L'application est développée avec Streamlit. L'utilisateur peut importer une image ou prendre une photo avec la caméra.

Après l'analyse, l'application affiche :

- la catégorie proposée ;
- le pourcentage de confiance ;
- les probabilités pour chaque classe ;
- un statut de fiabilité.

### 7. Résultats

Le modèle MobileNetV2 atteint environ **81,5 % de précision en validation**.

Les résultats sont bons pour certaines classes comme le carton, le verre ou le métal.

Les classes les plus difficiles sont le plastique, le papier et les déchets non recyclables, car elles peuvent se ressembler selon la photo.

### 8. Limites

Le modèle dépend fortement de la qualité de l'image. Une photo floue, sombre, mal cadrée ou avec plusieurs objets peut donner un mauvais résultat.

C'est pour cela que l'application affiche un statut de fiabilité. Si le modèle hésite, elle indique que la photo doit être vérifiée.

### 9. Conclusion

Pour conclure, WasteSort AI montre comment le Deep Learning peut être utilisé pour répondre à un problème concret : aider au tri des déchets.

Le projet combine un modèle d'intelligence artificielle, une interface web simple et une problématique environnementale.

## 2. Texte Oral À Apprendre

Bonjour à tous,

Aujourd'hui, je vais vous présenter mon projet **WasteSort AI**.

WasteSort AI est une application web qui permet de reconnaître automatiquement le type de déchet à partir d'une photo. L'idée est simple : l'utilisateur envoie une image d'un déchet, et l'application propose une catégorie de tri.

Ce projet part d'un problème concret. Le tri des déchets est important pour le recyclage, mais il n'est pas toujours évident de savoir dans quelle poubelle mettre un objet. Certains matériaux se ressemblent, comme le plastique et le papier, ou certains déchets non recyclables qui peuvent être confondus avec des objets recyclables.

L'objectif de mon projet est donc de créer un outil simple, visuel et facile à utiliser, capable d'aider l'utilisateur à mieux trier ses déchets.

Le système reconnaît six catégories : carton, verre, métal, papier, plastique et déchet non recyclable.

Pour développer ce projet, j'ai utilisé Python, TensorFlow, Keras et Streamlit. Le modèle principal est basé sur MobileNetV2, un modèle de reconnaissance d'images. J'ai utilisé le Transfer Learning, c'est-à-dire que j'ai repris un modèle déjà entraîné sur beaucoup d'images, puis je l'ai adapté au problème des déchets.

Au début, j'avais testé un CNN simple. Il permettait de classifier les images, mais les résultats étaient moins fiables sur des photos réelles. MobileNetV2 donne de meilleurs résultats, car il sait déjà extraire des formes, des couleurs et des textures importantes dans une image.

L'application web est faite avec Streamlit. L'utilisateur peut importer une image ou utiliser la caméra. Ensuite, l'application analyse l'image et affiche la catégorie proposée, le niveau de confiance, les probabilités pour chaque classe et un statut de fiabilité.

Le statut de fiabilité est important. Il peut indiquer "Très fiable", "Fiable", "À vérifier" ou "Incertain". Cela permet de ne pas donner une réponse trop sûre lorsque le modèle hésite.

Le modèle atteint environ 81,5 % de précision en validation. Les classes comme le carton, le verre et le métal sont souvent bien reconnues. En revanche, le plastique, le papier et les déchets non recyclables sont parfois plus difficiles à différencier, car ils peuvent se ressembler selon la photo.

Le projet a donc certaines limites. La qualité de l'image est très importante. Une photo floue, sombre, mal cadrée ou avec plusieurs objets peut réduire la fiabilité de la prédiction.

Pour améliorer ce projet, on pourrait ajouter plus d'images, utiliser des photos prises dans des conditions réelles, tester d'autres modèles comme EfficientNet ou créer une application mobile.

Pour conclure, WasteSort AI est un projet de Deep Learning appliqué à un cas concret et utile. Il montre comment l'intelligence artificielle peut aider dans un domaine lié à l'environnement, tout en restant simple à comprendre et facile à utiliser.

Merci pour votre attention.

## 3. Plan De Slides PowerPoint

### Slide 1 - Titre

**WasteSort AI**

Reconnaissance automatique des déchets avec Deep Learning

À mettre sur la slide :

- Nom du projet ;
- Nom de l'étudiant ;
- Classe ou formation ;
- Date ;
- Logo du projet.

### Slide 2 - Contexte

Titre : **Pourquoi ce projet ?**

Contenu :

- Le tri des déchets est important pour le recyclage.
- Beaucoup de personnes peuvent se tromper dans le tri.
- Les déchets peuvent se ressembler.
- L'intelligence artificielle peut aider à reconnaître les objets.

### Slide 3 - Problématique

Titre : **Problématique**

Question principale :

**Comment utiliser le Deep Learning pour reconnaître automatiquement un déchet à partir d'une photo ?**

À dire oralement :

Le but n'est pas seulement de prédire une classe, mais aussi d'indiquer si le modèle est sûr ou non de sa réponse.

### Slide 4 - Objectifs

Titre : **Objectifs Du Projet**

Contenu :

- Identifier le type de déchet à partir d'une image.
- Classer l'image en six catégories.
- Créer une interface simple.
- Afficher un niveau de confiance.
- Aider l'utilisateur à mieux trier.

### Slide 5 - Classes Reconnues

Titre : **Les 6 Catégories**

Contenu :

- Carton ;
- Verre ;
- Métal ;
- Papier ;
- Plastique ;
- Déchet non recyclable.

Conseil visuel :

Ajouter une petite icône ou image pour chaque classe.

### Slide 6 - Technologies

Titre : **Technologies Utilisées**

Contenu :

- Python ;
- TensorFlow / Keras ;
- MobileNetV2 ;
- Streamlit ;
- Scikit-learn ;
- Pillow ;
- Dataset Kaggle.

### Slide 7 - Dataset

Titre : **Dataset**

Contenu :

- Dataset : Garbage Classification ;
- Source : Kaggle ;
- Images réparties en plusieurs classes ;
- Utilisé pour entraîner et valider le modèle.

### Slide 8 - Méthodologie

Titre : **Méthode De Travail**

Contenu :

1. Récupération du dataset.
2. Prétraitement des images.
3. Data augmentation.
4. Entraînement du modèle.
5. Évaluation.
6. Création de l'interface.

### Slide 9 - Modèle MobileNetV2

Titre : **Pourquoi MobileNetV2 ?**

Contenu :

- Modèle léger et rapide ;
- Adapté à la reconnaissance d'images ;
- Déjà entraîné sur beaucoup d'images ;
- Réutilisé grâce au Transfer Learning ;
- Plus performant qu'un CNN simple.

### Slide 10 - Comparaison Des Modèles

Titre : **Pourquoi Ne Pas Utiliser MLP, RNN Ou Seq2Seq ?**

Contenu :

- MLP : possible, mais trop simple pour comprendre les formes d'une image ;
- CNN : adapté aux images, bonne première solution ;
- RNN : adapté aux séquences, pas idéal pour une image fixe ;
- Seq2Seq : adapté à la traduction ou génération de texte, pas à cette classification ;
- MobileNetV2 : meilleur choix ici grâce au Transfer Learning.

### Slide 11 - Interface Utilisateur

Titre : **Application Web**

Contenu :

- Upload d'image ;
- Utilisation de la caméra ;
- Résultat de prédiction ;
- Pourcentage de confiance ;
- Probabilités par classe ;
- Statut de fiabilité.

Conseil visuel :

Ajouter une capture d'écran de l'application.

### Slide 12 - Résultats

Titre : **Résultats**

Contenu :

- Modèle : MobileNetV2 ;
- Accuracy validation : environ 81,5 % ;
- Bonnes performances sur carton, verre et métal ;
- Classes plus difficiles : plastique, papier, trash.

### Slide 13 - Limites

Titre : **Limites**

Contenu :

- La photo doit être nette ;
- Un seul objet doit être visible ;
- Le fond doit être simple ;
- Certaines classes se ressemblent ;
- Le modèle n'est pas fiable à 100 %.

### Slide 14 - Améliorations Possibles

Titre : **Améliorations**

Contenu :

- Ajouter plus de données ;
- Utiliser plus d'images réelles ;
- Tester EfficientNet ;
- Ajouter une classe "objet inconnu" ;
- Créer une version mobile.

### Slide 15 - Conclusion

Titre : **Conclusion**

Contenu :

- Projet concret et utile ;
- IA appliquée à l'environnement ;
- Interface simple ;
- Résultats encourageants ;
- Projet améliorable avec plus de données.

## 4. Version Simple Pour Expliquer Au Jury

WasteSort AI est une application web qui aide à reconnaître le type de déchet à partir d'une photo.

L'utilisateur ajoute une image ou prend une photo avec la caméra. Ensuite, l'application analyse l'image et propose une catégorie : carton, verre, métal, papier, plastique ou déchet non recyclable.

Le modèle utilisé s'appelle MobileNetV2. C'est un modèle de Deep Learning adapté à la reconnaissance d'images. Il a été réentraîné pour reconnaître les déchets.

L'application affiche aussi un pourcentage de confiance. Si le modèle n'est pas sûr, elle indique que la photo doit être vérifiée.

Le projet montre comment l'intelligence artificielle peut être utilisée pour aider au tri des déchets, un problème concret lié à l'environnement.

## 5. Questions Possibles Du Jury Et Réponses

### Pourquoi avoir choisi ce sujet ?

J'ai choisi ce sujet parce qu'il combine intelligence artificielle et environnement. Le tri des déchets est un problème concret, facile à comprendre, et utile dans la vie quotidienne.

### Quel est l'objectif du projet ?

L'objectif est de créer une application capable de reconnaître un déchet à partir d'une photo et de proposer une catégorie de tri.

### Pourquoi utiliser MobileNetV2 ?

MobileNetV2 est léger, rapide et adapté à la reconnaissance d'images. Il donne de meilleurs résultats qu'un CNN simple, surtout grâce au Transfer Learning.

### Pourquoi ne pas utiliser un MLP ?

Un MLP peut fonctionner sur des pixels transformés en vecteur, mais il ne comprend pas bien la structure d'une image. Il perd les relations spatiales entre les pixels, donc il est moins adapté à la reconnaissance visuelle.

### Pourquoi ne pas utiliser un RNN ?

Un RNN est surtout utilisé pour des données séquentielles comme du texte, de l'audio ou des séries temporelles. Pour une image fixe de déchet, un CNN ou MobileNetV2 est plus adapté.

### Pourquoi ne pas utiliser Seq2Seq ?

Seq2Seq est utilisé quand l'entrée et la sortie sont des séquences, par exemple en traduction automatique. Ici, la sortie est simplement une classe parmi six catégories, donc Seq2Seq n'est pas nécessaire.

### C'est quoi le Transfer Learning ?

Le Transfer Learning consiste à utiliser un modèle déjà entraîné sur beaucoup d'images, puis à l'adapter à un nouveau problème. Dans ce projet, MobileNetV2 a été adapté pour reconnaître des déchets.

### Pourquoi le modèle n'est-il pas fiable à 100 % ?

Parce que les photos peuvent être très différentes : lumière, angle, qualité, fond, taille de l'objet. Certaines classes comme plastique, papier et trash peuvent aussi se ressembler.

### Comment le modèle donne-t-il une prédiction ?

Il analyse l'image, calcule une probabilité pour chaque classe, puis propose la classe avec la probabilité la plus élevée.

### À quoi sert le pourcentage de confiance ?

Il indique si le modèle est sûr de sa réponse. Si la confiance est faible, l'application affiche un statut comme "À vérifier" ou "Incertain".

### Quelles sont les limites du projet ?

La principale limite est la qualité de l'image. Une image floue, sombre, mal cadrée ou avec plusieurs objets peut provoquer une erreur.

### Comment améliorer le projet ?

On peut ajouter plus de données, utiliser des photos réelles, entraîner plus longtemps, tester d'autres modèles ou créer une application mobile.

### Est-ce que le projet peut être utilisé dans la vraie vie ?

Oui, mais il faudrait encore l'améliorer avec plus de données et le tester dans des conditions réelles avant une utilisation professionnelle.

## 6. Petite Conclusion À Dire À La Fin

Pour conclure, WasteSort AI est un projet qui montre comment l'intelligence artificielle peut aider dans un problème concret : le tri des déchets. Le modèle n'est pas parfait, mais il donne des résultats encourageants et l'application est simple à utiliser. Avec plus de données et quelques améliorations, ce type d'outil pourrait devenir une aide pratique pour mieux trier au quotidien.
