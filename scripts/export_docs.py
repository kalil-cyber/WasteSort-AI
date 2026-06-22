"""
export_docs.py
Génère les livrables PPTX et PDF pour WasteSort AI.
"""

from pathlib import Path
import re
import textwrap

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent.parent
EXPORTS = ROOT / "exports"
LOGO = ROOT / "assets" / "logo.svg"
REPORT = ROOT / "report.md"


SLIDES = [
    (
        "WasteSort AI",
        [
            "Reconnaissance automatique des déchets avec Deep Learning",
            "Application web simple pour aider au tri",
            "TensorFlow / Keras - MobileNetV2 - Streamlit",
        ],
    ),
    (
        "Pourquoi ce projet ?",
        [
            "Le tri des déchets est important pour le recyclage.",
            "Les utilisateurs peuvent se tromper entre plusieurs catégories.",
            "Une image peut aider à proposer rapidement une catégorie de tri.",
        ],
    ),
    (
        "Problématique",
        [
            "Comment reconnaître automatiquement un déchet à partir d'une photo ?",
            "Comment donner une réponse utile sans être trop sûr quand le modèle hésite ?",
        ],
    ),
    (
        "Objectifs",
        [
            "Identifier le type de déchet à partir d'une image.",
            "Classer l'image en six catégories.",
            "Afficher une confiance et des probabilités.",
            "Créer une interface simple pour un public non technique.",
        ],
    ),
    (
        "Catégories Reconnues",
        [
            "Carton",
            "Verre",
            "Métal",
            "Papier",
            "Plastique",
            "Déchet non recyclable",
        ],
    ),
    (
        "Technologies Utilisées",
        [
            "Python",
            "TensorFlow / Keras",
            "MobileNetV2 en Transfer Learning",
            "Streamlit",
            "Scikit-learn, Matplotlib et Pillow",
            "Dataset Kaggle Garbage Classification",
        ],
    ),
    (
        "Méthodologie",
        [
            "Organisation du dataset par classes.",
            "Prétraitement des images en 224 x 224 pixels.",
            "Data augmentation pour améliorer la robustesse.",
            "Entraînement MobileNetV2 puis fine-tuning.",
            "Évaluation avec accuracy et matrice de confusion.",
        ],
    ),
    (
        "Pourquoi MobileNetV2 ?",
        [
            "Modèle léger et rapide.",
            "Adapté à la reconnaissance d'images.",
            "Déjà entraîné sur beaucoup d'images.",
            "Plus fiable qu'un CNN simple sur les photos réelles.",
        ],
    ),
    (
        "Interface Utilisateur",
        [
            "Import d'image ou prise de photo.",
            "Affichage de la catégorie proposée.",
            "Pourcentage de confiance.",
            "Probabilités par classe.",
            "Statut : Très fiable, Fiable, À vérifier ou Incertain.",
        ],
    ),
    (
        "Résultats",
        [
            "Modèle principal : MobileNetV2.",
            "Accuracy validation : environ 81,5 %.",
            "Bonnes performances sur carton, verre et métal.",
            "Classes plus difficiles : plastique, papier et trash.",
        ],
    ),
    (
        "Limites",
        [
            "Le modèle dépend de la qualité de la photo.",
            "Une image floue ou mal cadrée peut provoquer une erreur.",
            "Certaines classes se ressemblent visuellement.",
            "Le modèle ne remplace pas totalement une vérification humaine.",
        ],
    ),
    (
        "Améliorations Possibles",
        [
            "Ajouter plus d'images réelles.",
            "Tester EfficientNet.",
            "Ajouter une classe objet inconnu.",
            "Créer une version mobile.",
            "Adapter les conseils de tri selon les règles locales.",
        ],
    ),
    (
        "Conclusion",
        [
            "WasteSort AI applique le Deep Learning à un problème concret.",
            "L'application est simple, visuelle et facile à présenter.",
            "Le projet montre le lien entre IA et environnement.",
            "Les résultats sont encourageants et améliorables avec plus de données.",
        ],
    ),
]


def clean_markdown(text: str) -> str:
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = text.replace("`", "")
    return text


def add_title(slide, title: str):
    box = slide.shapes.add_textbox(Inches(0.7), Inches(0.35), Inches(11.9), Inches(0.8))
    p = box.text_frame.paragraphs[0]
    p.text = title
    p.font.bold = True
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(15, 81, 50)


def add_footer(slide):
    box = slide.shapes.add_textbox(Inches(0.7), Inches(6.95), Inches(11.8), Inches(0.25))
    p = box.text_frame.paragraphs[0]
    p.text = "WasteSort AI - TensorFlow/Keras - MobileNetV2"
    p.font.size = Pt(9)
    p.font.color.rgb = RGBColor(100, 116, 139)
    p.alignment = PP_ALIGN.RIGHT


def add_ppt_logo(slide, left, top, size):
    box = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        left,
        top,
        size,
        size,
    )
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(255, 255, 255)
    box.line.color.rgb = RGBColor(232, 245, 233)
    box.line.width = Pt(2)

    circle = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.OVAL,
        left + size * 0.18,
        top + size * 0.16,
        size * 0.64,
        size * 0.64,
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(25, 135, 84)
    circle.line.color.rgb = RGBColor(25, 135, 84)

    leaf = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.OVAL,
        left + size * 0.28,
        top + size * 0.24,
        size * 0.44,
        size * 0.44,
    )
    leaf.fill.solid()
    leaf.fill.fore_color.rgb = RGBColor(116, 184, 74)
    leaf.line.color.rgb = RGBColor(116, 184, 74)

    text = slide.shapes.add_textbox(left + size * 0.20, top + size * 0.70, size * 0.60, size * 0.22)
    p = text.text_frame.paragraphs[0]
    p.text = "WS"
    p.alignment = PP_ALIGN.CENTER
    p.font.bold = True
    p.font.size = Pt(22)
    p.font.color.rgb = RGBColor(15, 81, 50)


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    for index, (title, bullets) in enumerate(SLIDES):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        background = slide.background.fill
        background.solid()
        background.fore_color.rgb = RGBColor(248, 250, 252)

        if index == 0:
            title_box = slide.shapes.add_textbox(Inches(0.9), Inches(1.1), Inches(7.2), Inches(1.0))
            p = title_box.text_frame.paragraphs[0]
            p.text = title
            p.font.bold = True
            p.font.size = Pt(46)
            p.font.color.rgb = RGBColor(15, 81, 50)

            subtitle_box = slide.shapes.add_textbox(Inches(0.95), Inches(2.25), Inches(7.4), Inches(2.1))
            tf = subtitle_box.text_frame
            for i, item in enumerate(bullets):
                para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                para.text = item
                para.font.size = Pt(22 if i == 0 else 18)
                para.font.color.rgb = RGBColor(51, 65, 85)
                para.space_after = Pt(10)

            add_ppt_logo(slide, Inches(9.0), Inches(1.25), Inches(2.45))
        else:
            add_title(slide, title)
            content = slide.shapes.add_textbox(Inches(1.0), Inches(1.45), Inches(11.0), Inches(4.9))
            tf = content.text_frame
            tf.word_wrap = True
            for i, item in enumerate(bullets):
                para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                para.text = item
                para.level = 0
                para.font.size = Pt(22)
                para.font.color.rgb = RGBColor(30, 41, 59)
                para.space_after = Pt(12)
                para.text = f"• {item}"

        add_footer(slide)

    output = EXPORTS / "WasteSort_AI_Presentation.pptx"
    prs.save(output)
    return output


def markdown_blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    buffer = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line.strip():
            if buffer:
                blocks.append("\n".join(buffer))
                buffer = []
            continue
        buffer.append(line)
    if buffer:
        blocks.append("\n".join(buffer))
    return blocks


def build_pdf():
    output = EXPORTS / "WasteSort_AI_Rapport.pdf"
    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.7 * cm,
    )
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0F5132"),
            fontSize=22,
            leading=28,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            textColor=colors.HexColor("#198754"),
            fontSize=15,
            leading=20,
            spaceBefore=12,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyTextClean",
            parent=styles["BodyText"],
            alignment=TA_LEFT,
            fontSize=10.5,
            leading=15,
            spaceAfter=7,
        )
    )

    story = []
    story.append(Paragraph("Rapport Professionnel - WasteSort AI", styles["DocTitle"]))
    story.append(Paragraph("Projet de reconnaissance d'images pour l'aide au tri des déchets", styles["BodyTextClean"]))
    story.append(Spacer(1, 0.3 * cm))

    for block in markdown_blocks(REPORT):
        block = clean_markdown(block)
        if block.startswith("# "):
            continue
        if block.startswith("## "):
            story.append(Paragraph(block[3:], styles["SectionTitle"]))
            continue
        if block.startswith("|"):
            rows = [row.strip("|").split("|") for row in block.splitlines() if row.startswith("|")]
            rows = [[cell.strip() for cell in row] for row in rows if "---" not in "".join(row)]
            if rows:
                table = Table(rows, hAlign="LEFT")
                table.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F5E9")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0F5132")),
                            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD5E1")),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ]
                    )
                )
                story.append(table)
                story.append(Spacer(1, 0.25 * cm))
            continue

        for paragraph in block.splitlines():
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if paragraph.startswith("- "):
                paragraph = "• " + paragraph[2:]
            if re.match(r"^\d+\. ", paragraph):
                paragraph = paragraph
            wrapped = "<br/>".join(textwrap.wrap(paragraph, width=105))
            story.append(Paragraph(wrapped, styles["BodyTextClean"]))

    story.append(PageBreak())
    story.append(Paragraph("Annexe - Résumé Pour Présentation", styles["DocTitle"]))
    story.append(
        Paragraph(
            "WasteSort AI est une application web qui utilise MobileNetV2 avec TensorFlow/Keras "
            "pour reconnaître six catégories de déchets à partir d'une photo. L'application affiche "
            "la prédiction, la confiance, les probabilités par classe et un statut de fiabilité.",
            styles["BodyTextClean"],
        )
    )
    doc.build(story)
    return output


def main():
    EXPORTS.mkdir(exist_ok=True)
    pptx_path = build_pptx()
    pdf_path = build_pdf()
    print(f"PPTX généré : {pptx_path}")
    print(f"PDF généré : {pdf_path}")


if __name__ == "__main__":
    main()
