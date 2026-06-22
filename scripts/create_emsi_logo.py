"""
create_emsi_logo.py
Crée une version propre du logo EMSI pour les documents.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "assets" / "emsi-logo-official.png"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main():
    width, height = 1200, 520
    green = (0, 145, 65)
    dark = (70, 70, 70)
    red = (220, 65, 40)

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    font_big = load_font("C:/Windows/Fonts/arialbd.ttf", 64)
    font_small = load_font("C:/Windows/Fonts/ariali.ttf", 28)
    font_honoris = load_font("C:/Windows/Fonts/cour.ttf", 34)
    font_bar = load_font("C:/Windows/Fonts/ariali.ttf", 58)
    font_emsi = load_font("C:/Windows/Fonts/timesbd.ttf", 64)

    # Groupe de silhouettes stylisé
    for box in ([60, 65, 100, 150], [105, 55, 145, 150], [150, 70, 190, 155], [195, 45, 240, 155]):
        draw.ellipse(box, fill=green)
    draw.rectangle([50, 145, 250, 265], fill=green)
    draw.polygon([(50, 145), (250, 145), (230, 260), (70, 260)], fill=green)

    # Bloc EMSI
    draw.rectangle([0, 285, 270, 360], fill=dark)
    draw.text((35, 285), "EMSI", font=font_emsi, fill="white")
    draw.polygon([(280, 250), (295, 235), (310, 250), (295, 265)], fill=red)

    # Texte principal
    draw.text((330, 50), "ECOLE MAROCAINE DES", font=font_big, fill=green)
    draw.text((330, 125), "SCIENCES DE L'INGENIEUR", font=font_big, fill=green)
    draw.text((330, 220), "Membre de", font=font_small, fill=dark)
    draw.rectangle([610, 235, 1130, 250], fill=dark)
    draw.text((330, 285), "HONORIS UNITED UNIVERSITIES", font=font_honoris, fill=dark)

    # Bandeau bas
    draw.rectangle([0, 405, width, height], fill=green)
    draw.text((110, 435), "Ecole Reconnue par l'Etat", font=font_bar, fill="white")

    OUTPUT.parent.mkdir(exist_ok=True)
    img.save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
