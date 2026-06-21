"""
streamlit_app.py
Interface Streamlit pour WasteSort AI.
"""

import importlib
import sys
from pathlib import Path

from PIL import Image
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
LOGO_PATH = ROOT / "assets" / "logo.svg"

from config import CLASS_LABELS_FR, MODEL_PATH, TRANSFER_MODEL_PATH  # noqa: E402
import inference as inference_module  # noqa: E402

inference_module = importlib.reload(inference_module)
load_model_and_classes = inference_module.load_model_and_classes
predict_from_pil = inference_module.predict_from_pil

st.set_page_config(
    page_title="WasteSort AI",
    page_icon="WS",
    layout="wide",
    initial_sidebar_state="expanded",
)

CLASS_COLORS = {
    "Carton": "#D4A574",
    "Verre": "#4FC3F7",
    "Métal": "#90A4AE",
    "Papier": "#FFF9C4",
    "Plastique": "#FF7043",
    "Déchet non recyclable": "#616161",
}

PRESENTATION_METRICS = {
    "Modèle principal": "MobileNetV2",
    "Validation": "81.5 %",
    "Classes": "6",
    "Outil": "TensorFlow / Keras",
}


def inject_css():
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        #MainMenu, footer, header, [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }
        .hero {
            background: linear-gradient(135deg, #0F5132 0%, #198754 55%, #20C997 100%);
            color: white;
            padding: 2rem;
            border-radius: 22px;
            margin-bottom: 1.4rem;
        }
        .hero-logo {
            width: 118px;
            height: 118px;
            background: white;
            border-radius: 28px;
            padding: 0.35rem;
            margin-bottom: 0.9rem;
            box-shadow: 0 12px 32px rgba(16, 24, 40, 0.18);
        }
        .hero-logo svg {
            width: 100%;
            height: 100%;
            display: block;
        }
        .hero p {
            font-size: 1.1rem;
            margin: 0;
            max-width: 820px;
        }
        .card {
            border: 1px solid #E8ECEF;
            background: #FFFFFF;
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 8px 24px rgba(16, 24, 40, 0.06);
            height: 100%;
        }
        .metric-card {
            text-align: center;
            border-radius: 16px;
            padding: 1rem;
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
        }
        .metric-card strong {
            display: block;
            color: #0F5132;
            font-size: 1.45rem;
            margin-bottom: 0.25rem;
        }
        .step-pill {
            display: inline-block;
            background: #E8F5E9;
            color: #0F5132;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .small-muted {
            color: #667085;
            font-size: 0.92rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_cards():
    cols = st.columns(len(PRESENTATION_METRICS))
    for col, (label, value) in zip(cols, PRESENTATION_METRICS.items()):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <strong>{value}</strong>
                    <span>{label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


def logo_html():
    if not LOGO_PATH.exists():
        return ""
    return f'<div class="hero-logo">{LOGO_PATH.read_text(encoding="utf-8")}</div>'


def reliability_label(confidence, margin):
    if confidence >= 0.9 and margin >= 0.25:
        return "Très fiable", "#198754"
    if confidence >= 0.75 and margin >= 0.15:
        return "Fiable", "#198754"
    if confidence >= 0.55:
        return "À vérifier", "#F59F00"
    return "Incertain", "#DC3545"


@st.cache_resource
def get_model(model_choice, model_mtime):
    path = TRANSFER_MODEL_PATH if model_choice == "transfer" else MODEL_PATH
    return load_model_and_classes(path)


def selected_model_mtime(model_choice):
    path = TRANSFER_MODEL_PATH if model_choice == "transfer" else MODEL_PATH
    return path.stat().st_mtime if path.exists() else 0


inject_css()

st.markdown(
    f"""
    <section class="hero">
        {logo_html()}
        <p>
            Une interface simple pour identifier le type de déchet à partir d'une photo
            et aider à mieux trier les matériaux recyclables.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)
metric_cards()
st.write("")

with st.sidebar:
    st.header("WasteSort AI")
    st.caption("Tri des déchets par reconnaissance d'image")
    st.markdown("---")
    model_choice = st.radio(
        "Modèle utilisé",
        options=["transfer", "cnn"],
        format_func=lambda x: "CNN simple" if x == "cnn" else "MobileNetV2 (Transfer)",
        help="MobileNetV2 est recommandé pour les photos réelles.",
    )
    st.success("MobileNetV2 est le modèle conseillé.")
    st.markdown("---")
    st.markdown("**Classes reconnues**")
    for label in CLASS_LABELS_FR.values():
        st.markdown(f"- {label}")
    st.markdown("---")
    st.markdown("**Conseil photo**")
    st.caption("Photo nette, un seul objet, fond simple, objet centré.")

try:
    model, index_to_class = get_model(model_choice, selected_model_mtime(model_choice))
    model_loaded = True
except FileNotFoundError as e:
    model_loaded = False
    st.error(str(e))
    st.info(
        "1. Téléchargez le dataset Kaggle « Garbage Classification »\n"
        "2. Placez les images dans `data/garbage/`\n"
        "3. Lancez `python src/train.py`"
    )

if model_loaded:
    demo_tab, method_tab = st.tabs(["Démonstration", "Comment ça marche"])

    with demo_tab:
        st.subheader("Tester une image")
        st.markdown(
            "Ajoutez une photo de déchet ou utilisez la caméra. L'interface retourne "
            "la classe prédite, le niveau de confiance et les probabilités par catégorie."
        )

        col_upload, col_result = st.columns([1, 1.15], gap="large")

        with col_upload:
            st.markdown('<span class="step-pill">Étape 1</span>', unsafe_allow_html=True)
            input_mode = st.radio(
                "Source de l'image",
                ["Téléverser une image", "Utiliser la caméra"],
                horizontal=True,
            )

            uploaded = None
            camera = None
            if input_mode == "Téléverser une image":
                uploaded = st.file_uploader(
                    "Choisissez une image JPG ou PNG",
                    type=["jpg", "jpeg", "png"],
                )
            else:
                camera = st.camera_input("Prenez une photo")

            image_source = uploaded or camera

            st.markdown("**Pour une meilleure prédiction**")
            st.markdown(
                "- Un seul déchet visible\n"
                "- Objet centré et assez proche\n"
                "- Fond simple\n"
                "- Bonne luminosité"
            )

            if image_source:
                img = Image.open(image_source)
                st.image(img, caption="Image envoyée", use_container_width=True)

        with col_result:
            st.markdown('<span class="step-pill">Étape 2</span>', unsafe_allow_html=True)
            st.subheader("Résultat de l'analyse")
            if image_source:
                with st.spinner("Analyse de l'image en cours..."):
                    result = predict_from_pil(img, model, index_to_class)

                label = result["label_fr"]
                confidence = result["confidence"]
                margin = result.get("margin", 0.0)
                color = CLASS_COLORS.get(label, "#198754")
                reliability, reliability_color = reliability_label(confidence, margin)
                accepted = reliability in {"Très fiable", "Fiable"}
                title_label = label if accepted else "Photo à vérifier"

                st.markdown(
                    f"""
                    <div style="
                        background: {color}20;
                        border: 1px solid {color}55;
                        border-left: 7px solid {color};
                        padding: 1.4rem;
                        border-radius: 18px;
                        margin-bottom: 1rem;
                    ">
                        <p class="small-muted" style="margin:0;">Résultat</p>
                        <h2 style="margin:0.15rem 0; color:{color};">{title_label}</h2>
                        <p style="margin:0.25rem 0 0;">
                            Proposition du modèle : <strong>{label}</strong>
                        </p>
                        <p style="margin:0.35rem 0 0; font-size:1.15rem;">
                            Confiance : <strong>{confidence:.1%}</strong>
                        </p>
                        <p style="margin:0.2rem 0 0; font-size:0.95rem;">
                            Écart avec la 2e classe : <strong>{margin:.1%}</strong>
                        </p>
                        <p style="margin:0.35rem 0 0; color:{reliability_color};">
                            Statut : <strong>{reliability}</strong>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if reliability in {"À vérifier", "Incertain"}:
                    st.warning(
                        "Le modèle n'est pas assez sûr pour valider ce tri. "
                        "Reprenez une photo plus nette, avec un seul déchet au centre."
                    )
                else:
                    st.success("La prédiction est assez stable pour être utilisée.")

                st.markdown("**Probabilités par classe**")
                sorted_probs = sorted(
                    result["probabilities"].items(),
                    key=lambda x: x[1],
                    reverse=True,
                )
                for class_name, prob in sorted_probs:
                    st.progress(prob, text=f"{class_name} - {prob:.1%}")
            else:
                st.info("Ajoutez une image pour lancer l'analyse.")

    with method_tab:
        st.subheader("Comment fonctionne WasteSort AI ?")
        col_1, col_2, col_3 = st.columns(3)
        with col_1:
            st.markdown(
                """
                <div class="card">
                    <h3>1. Prendre une photo</h3>
                    <p>Ajoutez une image claire avec un seul déchet bien visible.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_2:
            st.markdown(
                """
                <div class="card">
                    <h3>2. Analyser l'image</h3>
                    <p>L'application observe la forme, la couleur et la texture du déchet.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col_3:
            st.markdown(
                """
                <div class="card">
                    <h3>3. Proposer le tri</h3>
                    <p>Elle indique la catégorie la plus probable et affiche le niveau de confiance.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### Pourquoi MobileNetV2 ?")
        st.write(
            "MobileNetV2 est léger, rapide et adapté à une interface web. "
            "Il a été adapté aux images de déchets pour distinguer les six catégories."
        )
        st.markdown("### Performance actuelle")
        st.info(
            "Le modèle MobileNetV2 atteint environ 81,5 % de validation sur le dataset Kaggle. "
            "Les classes les plus ambiguës restent plastic, trash et parfois paper, car leurs "
            "apparences peuvent se ressembler selon la photo."
        )

    st.markdown("---")
    st.caption("WasteSort AI - TensorFlow/Keras | MobileNetV2")
