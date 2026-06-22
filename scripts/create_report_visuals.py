"""
create_report_visuals.py
Crée les captures et diagrammes utilisés dans le rapport.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

GREEN = (15, 81, 50)
LIGHT_GREEN = (232, 245, 233)
ACCENT = (25, 135, 84)
MINT = (116, 184, 74)
DARK = (30, 41, 59)
MUTED = (100, 116, 139)
BLUE = (59, 130, 246)
ORANGE = (245, 158, 11)
RED = (220, 53, 69)
WHITE = (255, 255, 255)
BG = (248, 250, 252)


def font(size, bold=False):
    path = "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def rounded(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def arrow(draw, start, end, color=ACCENT, width=5):
    draw.line([start, end], fill=color, width=width)
    x1, y1 = start
    x2, y2 = end
    if x2 > x1:
        points = [(x2, y2), (x2 - 16, y2 - 10), (x2 - 16, y2 + 10)]
    elif y2 > y1:
        points = [(x2, y2), (x2 - 10, y2 - 16), (x2 + 10, y2 - 16)]
    else:
        points = [(x2, y2), (x2 + 16, y2 - 10), (x2 + 16, y2 + 10)]
    draw.polygon(points, fill=color)


def center_text(draw, box, text, fnt, fill=DARK):
    x1, y1, x2, y2 = box
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - tw) / 2, y1 + (y2 - y1 - th) / 2), text, font=fnt, fill=fill)


def draw_title(draw, title, subtitle=None):
    draw.text((60, 35), title, font=font(34, True), fill=GREEN)
    if subtitle:
        draw.text((60, 82), subtitle, font=font(18), fill=MUTED)


def create_app_capture():
    img = Image.new("RGB", (1400, 850), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Capture du projet WasteSort AI", "Interface de prédiction utilisée pour la démonstration")

    # Browser/app frame
    rounded(d, (55, 125, 1345, 800), 24, WHITE, (226, 232, 240), 2)
    d.rectangle((55, 125, 1345, 175), fill=(241, 245, 249))
    for i, color in enumerate([(239, 68, 68), (245, 158, 11), (34, 197, 94)]):
        d.ellipse((80 + i * 30, 142, 98 + i * 30, 160), fill=color)
    d.text((180, 142), "localhost:8501 - WasteSort AI", font=font(17), fill=MUTED)

    # Sidebar
    rounded(d, (85, 205, 360, 760), 18, (250, 252, 250), (226, 232, 240), 2)
    d.text((115, 230), "WasteSort AI", font=font(27, True), fill=GREEN)
    d.text((115, 268), "Tri des déchets par image", font=font(15), fill=MUTED)
    d.line((115, 305, 330, 305), fill=(226, 232, 240), width=2)
    d.text((115, 330), "Modèle utilisé", font=font(17, True), fill=DARK)
    rounded(d, (115, 365, 325, 415), 14, LIGHT_GREEN, ACCENT, 2)
    d.text((138, 379), "MobileNetV2", font=font(18, True), fill=GREEN)
    d.text((115, 455), "Classes reconnues", font=font(17, True), fill=DARK)
    classes = ["Carton", "Verre", "Métal", "Papier", "Plastique", "Déchet non recyclable"]
    for idx, cls in enumerate(classes):
        d.text((130, 492 + idx * 34), f"• {cls}", font=font(16), fill=DARK)

    # Hero
    rounded(d, (395, 205, 1310, 340), 22, GREEN)
    d.text((430, 238), "WasteSort AI", font=font(42, True), fill=WHITE)
    d.text((430, 292), "Identifier un déchet à partir d'une photo", font=font(22), fill=(220, 252, 231))

    # Upload panel
    rounded(d, (395, 375, 805, 735), 18, WHITE, (226, 232, 240), 2)
    d.text((430, 405), "Étape 1", font=font(18, True), fill=ACCENT)
    d.text((430, 445), "Importer ou prendre une photo", font=font(23, True), fill=DARK)
    rounded(d, (450, 500, 750, 675), 18, (239, 246, 255), BLUE, 2)
    d.rectangle((520, 555, 680, 625), outline=BLUE, width=5)
    d.ellipse((570, 528, 630, 588), outline=BLUE, width=5)
    d.text((488, 640), "Image envoyée", font=font(17), fill=MUTED)

    # Result panel
    rounded(d, (845, 375, 1310, 735), 18, WHITE, (226, 232, 240), 2)
    d.text((880, 405), "Étape 2", font=font(18, True), fill=ACCENT)
    d.text((880, 445), "Résultat de l'analyse", font=font(23, True), fill=DARK)
    rounded(d, (885, 500, 1265, 615), 16, LIGHT_GREEN, ACCENT, 4)
    d.text((915, 525), "Classe proposée : Carton", font=font(24, True), fill=GREEN)
    d.text((915, 565), "Confiance : 94,2 %  |  Statut : Fiable", font=font(18), fill=DARK)
    bars = [("Carton", 0.94, ACCENT), ("Papier", 0.03, ORANGE), ("Plastique", 0.02, BLUE)]
    for i, (label, value, color) in enumerate(bars):
        y = 650 + i * 28
        d.text((900, y), label, font=font(14), fill=DARK)
        d.rectangle((980, y + 4, 1240, y + 18), fill=(226, 232, 240))
        d.rectangle((980, y + 4, 980 + int(260 * value), y + 18), fill=color)

    img.save(ASSETS / "report-app-capture.png")


def create_pipeline_diagram():
    img = Image.new("RGB", (1400, 700), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Diagramme de fonctionnement", "De la photo utilisateur jusqu'au résultat affiché")
    steps = [
        ("Photo", "Image envoyée"),
        ("Prétraitement", "224 x 224 px"),
        ("MobileNetV2", "Analyse visuelle"),
        ("Probabilités", "6 classes"),
        ("Résultat", "Confiance + statut"),
    ]
    x = 80
    y = 255
    w = 210
    h = 120
    for i, (title, subtitle) in enumerate(steps):
        rounded(d, (x, y, x + w, y + h), 18, WHITE, ACCENT, 3)
        center_text(d, (x, y + 18, x + w, y + 60), title, font(24, True), GREEN)
        center_text(d, (x, y + 62, x + w, y + 105), subtitle, font(16), MUTED)
        if i < len(steps) - 1:
            arrow(d, (x + w + 15, y + h // 2), (x + w + 80, y + h // 2))
        x += 265
    img.save(ASSETS / "report-diagram-pipeline.png")


def create_architecture_diagram():
    img = Image.new("RGB", (1400, 760), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Architecture du modèle", "MobileNetV2 utilisé en Transfer Learning")
    layers = [
        ("Image", "224 x 224 x 3"),
        ("MobileNetV2", "Extraction des caractéristiques"),
        ("GlobalAveragePooling2D", "Réduction des cartes"),
        ("Dense + ReLU", "Apprentissage final"),
        ("Dropout", "Réduction du surapprentissage"),
        ("Softmax", "6 probabilités"),
    ]
    y = 150
    for i, (title, subtitle) in enumerate(layers):
        color = GREEN if i in {1, 5} else ACCENT
        rounded(d, (250, y, 1150, y + 70), 16, WHITE, color, 3)
        d.text((290, y + 15), title, font=font(22, True), fill=color)
        d.text((650, y + 20), subtitle, font=font(18), fill=DARK)
        if i < len(layers) - 1:
            arrow(d, (700, y + 78), (700, y + 112), color=color)
        y += 105
    img.save(ASSETS / "report-diagram-architecture.png")


def create_training_diagram():
    img = Image.new("RGB", (1400, 760), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Diagramme d'entraînement", "Organisation des données et entraînement du modèle")
    steps = [
        ("Dataset Kaggle", "Images classées par dossier"),
        ("Train / Validation", "Séparation des données"),
        ("Data augmentation", "Variations pour généraliser"),
        ("Phase 1", "Tête du modèle entraînée"),
        ("Phase 2", "Fine-tuning MobileNetV2"),
        ("Évaluation", "Accuracy, rapport, matrice"),
    ]
    positions = [(80, 180), (500, 180), (920, 180), (80, 470), (500, 470), (920, 470)]
    for i, ((title, subtitle), (x, y)) in enumerate(zip(steps, positions)):
        rounded(d, (x, y, x + 330, y + 130), 20, WHITE, ACCENT, 3)
        d.text((x + 25, y + 30), title, font=font(23, True), fill=GREEN)
        d.text((x + 25, y + 72), subtitle, font=font(16), fill=DARK)
    for start, end in [((410, 245), (500, 245)), ((830, 245), (920, 245)), ((1085, 310), (1085, 470)), ((920, 535), (830, 535)), ((500, 535), (410, 535))]:
        arrow(d, start, end)
    img.save(ASSETS / "report-diagram-training.png")


def create_results_chart():
    img = Image.new("RGB", (1400, 720), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Synthèse des résultats", "Performance de validation et classes difficiles")
    rounded(d, (70, 145, 1330, 640), 22, WHITE, (226, 232, 240), 2)
    d.text((120, 200), "Accuracy validation", font=font(24, True), fill=DARK)
    d.arc((120, 260, 420, 560), 135, 135 + int(270 * 0.815), fill=ACCENT, width=28)
    d.arc((120, 260, 420, 560), 135 + int(270 * 0.815), 405, fill=(226, 232, 240), width=28)
    center_text(d, (120, 330, 420, 470), "81,5 %", font(42, True), GREEN)
    d.text((560, 200), "Classes plus stables", font=font(24, True), fill=GREEN)
    for i, label in enumerate(["Carton", "Verre", "Métal"]):
        rounded(d, (560, 255 + i * 72, 850, 310 + i * 72), 14, LIGHT_GREEN, ACCENT, 2)
        d.text((585, 270 + i * 72), label, font=font(20, True), fill=GREEN)
    d.text((940, 200), "Classes à améliorer", font=font(24, True), fill=ORANGE)
    for i, label in enumerate(["Plastique", "Papier", "Trash"]):
        rounded(d, (940, 255 + i * 72, 1230, 310 + i * 72), 14, (255, 247, 237), ORANGE, 2)
        d.text((965, 270 + i * 72), label, font=font(20, True), fill=(154, 52, 18))
    img.save(ASSETS / "report-results-summary.png")


def create_model_comparison():
    img = Image.new("RGB", (1400, 760), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Comparaison des modèles", "Pourquoi MobileNetV2 est le meilleur choix pour ce projet")

    models = [
        ("MLP", "Simple", "Perd la structure de l'image", ORANGE),
        ("CNN", "Adapté aux images", "Bonne base pour la vision", ACCENT),
        ("RNN", "Séquences", "Texte, audio, séries temporelles", BLUE),
        ("Seq2Seq", "Séquence vers séquence", "Traduction, résumé, chatbot", RED),
        ("MobileNetV2", "Images + Transfer Learning", "Choix principal du projet", GREEN),
    ]

    x_positions = [60, 325, 590, 855, 1120]
    for x, (name, role, note, color) in zip(x_positions, models):
        rounded(d, (x, 180, x + 220, 560), 24, WHITE, color, 4)
        d.ellipse((x + 70, 220, x + 150, 300), fill=color)
        center_text(d, (x + 55, 315, x + 165, 360), name, font(26, True), color)
        center_text(d, (x + 20, 380, x + 200, 430), role, font(17, True), DARK)
        wrapped = note.split(" ")
        line1 = " ".join(wrapped[:3])
        line2 = " ".join(wrapped[3:])
        center_text(d, (x + 20, 450, x + 200, 485), line1, font(14), MUTED)
        center_text(d, (x + 20, 485, x + 200, 525), line2, font(14), MUTED)

    d.text((445, 625), "Conclusion : pour une image fixe, les modèles de vision comme CNN et MobileNetV2 sont les plus adaptés.", font=font(22, True), fill=GREEN)
    img.save(ASSETS / "report-model-comparison.png")


def main():
    ASSETS.mkdir(exist_ok=True)
    create_app_capture()
    create_pipeline_diagram()
    create_architecture_diagram()
    create_training_diagram()
    create_results_chart()
    create_model_comparison()
    print("Visuels du rapport générés.")


if __name__ == "__main__":
    main()
