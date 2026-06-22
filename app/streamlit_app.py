"""
streamlit_app.py
Interface Streamlit pour EcoSmart Campus AI.
"""

import importlib
import sys
from pathlib import Path

from PIL import Image
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
LOGO_PATH = ROOT / "assets" / "logo.svg"
LOGO_PNG_PATH = ROOT / "assets" / "wastesort-suite-logo-clear.png"
EMSI_LOGO_PATH = ROOT / "assets" / "emsi-logo-official.png"

from campus_ai import EcoScoreInput, answer_question, forecast_energy, model_catalog, predict_eco_score  # noqa: E402
from config import CLASS_LABELS_FR, MODEL_PATH, TRANSFER_MODEL_PATH  # noqa: E402
import inference as inference_module  # noqa: E402

inference_module = importlib.reload(inference_module)
load_model_and_classes = inference_module.load_model_and_classes
predict_from_pil = inference_module.predict_from_pil


st.set_page_config(
    page_title="WasteSort AI Suite",
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


def inject_css():
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }
        #MainMenu, footer {
            visibility: hidden;
            height: 0;
        }
        .hero {
            background: linear-gradient(135deg, #0F5132 0%, #198754 55%, #20C997 100%);
            color: white;
            padding: 2rem;
            border-radius: 22px;
            margin-bottom: 1.3rem;
        }
        .hero h1 {
            margin: 0 0 0.45rem 0;
            font-size: 2.6rem;
        }
        .hero p {
            margin: 0;
            font-size: 1.1rem;
            max-width: 850px;
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
            font-size: 1.4rem;
            margin-bottom: 0.25rem;
        }
        .model-card {
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 1rem;
            background: white;
            min-height: 180px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def image_html(path: Path, width=90):
    if not path.exists():
        return ""
    return f'<img src="data:image/svg+xml;utf8,{path.read_text(encoding="utf-8")}" width="{width}" />'


def metric_cards():
    metrics = {
        "Images": "MobileNetV2",
        "Tableaux": "MLP",
        "Séries": "LSTM",
        "Texte": "Seq2Seq",
    }
    cols = st.columns(len(metrics))
    for col, (label, value) in zip(cols, metrics.items()):
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


def reliability_label(confidence, margin):
    if confidence >= 0.9 and margin >= 0.25:
        return "Très fiable", "#198754"
    if confidence >= 0.75 and margin >= 0.15:
        return "Fiable", "#198754"
    if confidence >= 0.55:
        return "À vérifier", "#F59F00"
    return "Incertain", "#DC3545"


@st.cache_resource
def get_waste_model(model_choice, model_mtime):
    path = TRANSFER_MODEL_PATH if model_choice == "transfer" else MODEL_PATH
    return load_model_and_classes(path)


def selected_model_mtime(model_choice):
    path = TRANSFER_MODEL_PATH if model_choice == "transfer" else MODEL_PATH
    return path.stat().st_mtime if path.exists() else 0


def render_sidebar():
    with st.sidebar:
        if LOGO_PNG_PATH.exists():
            st.image(str(LOGO_PNG_PATH), width=190)
        elif LOGO_PATH.exists():
            st.markdown(image_html(LOGO_PATH, width=145), unsafe_allow_html=True)
        st.header("WasteSort AI Suite")
        st.caption("Plateforme IA multi-modèles pour le tri et l'écologie")
        st.markdown("---")
        page = st.radio(
            "Navigation",
            [
                "Accueil",
                "Déchets - CNN/MobileNetV2",
                "Score écologique - MLP",
                "Prévision énergie - LSTM",
                "Assistant tri - Seq2Seq",
                "Comparaison des modèles",
            ],
        )
        st.markdown("---")
        st.caption("Projet basé sur WasteSort AI et étendu avec MLP, LSTM et Seq2Seq.")
        return page


def render_home():
    if LOGO_PNG_PATH.exists():
        col_logo, col_title = st.columns([1, 4], vertical_alignment="center")
        with col_logo:
            st.image(str(LOGO_PNG_PATH), width=145)
        with col_title:
            st.markdown("## WasteSort AI Suite")
            st.caption("Plateforme IA multi-modèles pour le tri et l'écologie")

    st.markdown(
        """
        <section class="hero">
            <h1>WasteSort AI Suite</h1>
            <p>
                Une plateforme intelligente qui regroupe plusieurs modèles d'IA autour du tri,
                de l'écologie, de la prévision et de l'assistance utilisateur.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )
    metric_cards()
    st.subheader("Objectif")
    st.write(
        "Le projet transforme WasteSort AI en une suite complète : reconnaissance d'images, "
        "score écologique, prévision de consommation et assistant de tri. Chaque module montre "
        "un type de modèle différent."
    )

    cols = st.columns(4)
    modules = model_catalog()
    for col, item in zip(cols, modules):
        with col:
            st.markdown(
                f"""
                <div class="model-card">
                    <h3>{item['name']}</h3>
                    <p><strong>Données :</strong> {item['data']}</p>
                    <p><strong>Module :</strong> {item['module']}</p>
                    <p>{item['role']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_waste_classifier():
    st.subheader("Reconnaissance des déchets - CNN / MobileNetV2")
    st.write("Ce module garde le cœur du projet WasteSort AI : classer une photo de déchet.")

    model_choice = st.radio(
        "Modèle utilisé",
        options=["transfer", "cnn"],
        format_func=lambda x: "CNN simple" if x == "cnn" else "MobileNetV2 (Transfer)",
        horizontal=True,
    )

    try:
        model, index_to_class = get_waste_model(model_choice, selected_model_mtime(model_choice))
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    col_upload, col_result = st.columns([1, 1.15], gap="large")
    with col_upload:
        input_mode = st.radio("Source de l'image", ["Téléverser une image", "Utiliser la caméra"], horizontal=True)
        image_source = None
        if input_mode == "Téléverser une image":
            image_source = st.file_uploader("Choisissez une image JPG ou PNG", type=["jpg", "jpeg", "png"])
        else:
            image_source = st.camera_input("Prenez une photo")

        st.info("Conseil : une photo nette, un seul déchet, fond simple.")
        if image_source:
            img = Image.open(image_source)
            st.image(img, caption="Image analysée", use_container_width=True)

    with col_result:
        st.markdown("### Résultat")
        if not image_source:
            st.info("Ajoutez une image pour lancer l'analyse.")
            return

        with st.spinner("Analyse en cours..."):
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
            <div style="background:{color}20;border-left:7px solid {color};padding:1.2rem;border-radius:16px;">
                <p style="margin:0;color:#64748B;">Résultat</p>
                <h2 style="margin:0.2rem 0;color:{color};">{title_label}</h2>
                <p>Proposition : <strong>{label}</strong></p>
                <p>Confiance : <strong>{confidence:.1%}</strong></p>
                <p>Écart avec la 2e classe : <strong>{margin:.1%}</strong></p>
                <p style="color:{reliability_color};">Statut : <strong>{reliability}</strong></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not accepted:
            st.warning("Le modèle hésite. Reprenez une photo plus nette avant de valider le tri.")
        else:
            st.success("La prédiction est assez stable pour être utilisée.")

        st.markdown("### Probabilités par classe")
        for class_name, prob in sorted(result["probabilities"].items(), key=lambda item: item[1], reverse=True):
            st.progress(prob, text=f"{class_name} - {prob:.1%}")


def render_eco_score():
    st.subheader("Score écologique - MLP")
    st.write(
        "Ce module représente un MLP sur données tabulaires : il combine plusieurs variables "
        "pour produire un score écologique."
    )
    col_inputs, col_result = st.columns(2)
    with col_inputs:
        recycled_items = st.slider("Déchets correctement triés cette semaine", 0, 60, 25)
        electricity_kwh = st.slider("Consommation électrique estimée (kWh)", 0, 350, 120)
        water_liters = st.slider("Consommation d'eau estimée (litres)", 0, 5000, 1800)
        participation = st.slider("Participation aux actions écologiques", 0, 10, 6)
        transport_score = st.slider("Transport durable", 0, 10, 7)

    with col_result:
        result = predict_eco_score(
            EcoScoreInput(
                recycled_items=recycled_items,
                electricity_kwh=electricity_kwh,
                water_liters=water_liters,
                participation=participation,
                transport_score=transport_score,
            )
        )
        st.metric("Score écologique", f"{result['score']}/100", result["label"])
        st.markdown("### Détail du score")
        for label, value in result["details"].items():
            st.progress(value / 35 if label == "Tri" else min(value / 25, 1), text=f"{label} : {value}")


def render_energy_forecast():
    st.subheader("Prévision énergie - RNN / LSTM")
    st.write(
        "Ce module illustre une logique RNN/LSTM : utiliser l'historique des jours précédents "
        "pour prédire les prochains jours."
    )
    default_history = "120, 128, 125, 132, 140, 137, 145"
    history_text = st.text_input("Historique de consommation (kWh, séparé par virgules)", default_history)
    days = st.slider("Nombre de jours à prédire", 3, 14, 7)

    try:
        history = [float(value.strip()) for value in history_text.split(",") if value.strip()]
        forecast = forecast_energy(history, days=days)
    except ValueError as exc:
        st.error(str(exc))
        return

    st.metric("Prévision moyenne", f"{sum(forecast) / len(forecast):.1f} kWh")
    chart_data = {"Historique": history + [None] * days, "Prévision": [None] * len(history) + forecast}
    st.line_chart(chart_data)
    st.write("Prévisions :", forecast)


def render_chatbot():
    st.subheader("Assistant de tri - Seq2Seq / FAQ")
    st.write(
        "Ce module illustre un assistant conversationnel. Dans une version avancée, un Seq2Seq "
        "générerait les réponses ; ici, le prototype répond de manière fiable à partir d'une base FAQ."
    )
    question = st.text_input("Posez une question", "Où jeter une bouteille plastique ?")
    result = answer_question(question)
    st.markdown("### Réponse")
    st.success(result["answer"])
    st.caption(f"Sujet détecté : {result['matched_topic']} | confiance : {result['confidence']:.0%}")

    st.markdown("### Exemples de questions")
    st.write("- Où jeter du carton ?")
    st.write("- Comment réduire l'énergie ?")
    st.write("- Où mettre une bouteille en verre ?")


def render_model_comparison():
    st.subheader("Comparaison des modèles")
    st.write("Chaque modèle correspond à un type de donnée différent.")
    for item in model_catalog():
        with st.container(border=True):
            st.markdown(f"### {item['name']}")
            st.write(f"**Type de données :** {item['data']}")
            st.write(f"**Module dans le projet :** {item['module']}")
            st.write(item["role"])

    st.info(
        "Conclusion : MobileNetV2 reste le meilleur choix pour les images, mais MLP, LSTM "
        "et Seq2Seq complètent la plateforme pour les données tabulaires, temporelles et textuelles."
    )


def main():
    inject_css()
    page = render_sidebar()
    if page == "Accueil":
        render_home()
    elif page == "Déchets - CNN/MobileNetV2":
        render_waste_classifier()
    elif page == "Score écologique - MLP":
        render_eco_score()
    elif page == "Prévision énergie - LSTM":
        render_energy_forecast()
    elif page == "Assistant tri - Seq2Seq":
        render_chatbot()
    else:
        render_model_comparison()


if __name__ == "__main__":
    main()
