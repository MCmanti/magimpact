import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import json

# Intégrer le token directement dans le code
os.environ["DATABRICKS_TOKEN"] = "dapic18ea4067f8260fc6a71cbcc86748a0d-3"  # Remplacez par votre token Databricks

# Fonction pour interagir avec l'endpoint
ENDPOINT_URL = "https://adb-4282284702815533.13.azuredatabricks.net/serving-endpoints/magimpact/invocations" 

def score_model(dataset):
    headers = {
        'Authorization': f'Bearer {os.environ.get("DATABRICKS_TOKEN")}',
        'Content-Type': 'application/json'
    }
    data_json = json.dumps({"dataframe_split": dataset.to_dict(orient='split')}, allow_nan=True)
    response = requests.request(method='POST', headers=headers, url=ENDPOINT_URL, data=data_json)
    if response.status_code != 200:
        raise Exception(f'Request failed with status {response.status_code}, {response.text}')
    return response.json()

# Configuration de l'application Streamlit
st.title("Prédiction pour Wear Parts")
st.sidebar.header("Paramètres")

# Sélection du type de pièce
wearpart_type = st.sidebar.selectbox("Type de Wear Part", ["Impeller", "Anvil"])

# Static input obligatoire
static_input = "Averge lifetime wear part"

# Champs communs
common_fields = {
    "Tip Speed": st.number_input("Tip Speed", value=0.0),
    "Number of impellers": st.number_input("Number of impellers", value=0),
    "Flow rate": st.number_input("Flow rate", value=0.0),
    "Abrasivity": st.number_input("Abrasivity", value=0.0),
    "Density": st.number_input("Density", value=0.0),
    "Crushability": st.number_input("Crushability", value=0.0),
    "Weight": st.number_input("Weight", value=0.0),
    "DF 90": st.number_input("DF 90", value=0.0),
    "DF 50": st.number_input("DF 50", value=0.0),
    "DF 10": st.number_input("DF 10", value=0.0),
    "DP 90": st.number_input("DP 90", value=0.0),
    "DP 50": st.number_input("DP 50", value=0.0),
    "DP 10": st.number_input("DP 10", value=0.0),
    "Return Percentage": st.number_input("Return Percentage", value=0.0),
}

# Listes déroulantes pour les champs spécifiques
if wearpart_type == "Impeller":
    design_choice = st.selectbox("Design", ["None", "Flat", "Flat - 2 layers", "Pocket"])
    material_choice = st.selectbox("Type of Material", ["None", "GRAVEL"])
    specific_fields = {
        "Table Diameter": st.number_input("Table Diameter", value=0.0),
        "Design_Flat": 1 if design_choice == "Flat" else 0,
        "Design_Flat - 2 layers": 1 if design_choice == "Flat - 2 layers" else 0,
        "Design_Pocket": 1 if design_choice == "Pocket" else 0,
        "Type_of_material_cat_GRAVEL": 1 if material_choice == "GRAVEL" else 0,
    }
elif wearpart_type == "Anvil":
    wearpart_choice = st.selectbox("Type of Wear Part", ["None", "QCA-054", "QCA-054H", "QCA-213", "QCA-218"])
    ceramic_choice = st.selectbox("Ceramic", ["None", "Yes", "No"])
    material_choice = st.selectbox("Type of Material", ["None", "GRAVEL", "NO_GRAVEL"])
    specific_fields = {
        "Type of wear part_QCA-054": 1 if wearpart_choice == "QCA-054" else 0,
        "Type of wear part_QCA-054H": 1 if wearpart_choice == "QCA-054H" else 0,
        "Type of wear part_QCA-213": 1 if wearpart_choice == "QCA-213" else 0,
        "Type of wear part_QCA-218": 1 if wearpart_choice == "QCA-218" else 0,
        "Ceramic_No": 1 if ceramic_choice == "No" else 0,
        "Ceramic_Yes": 1 if ceramic_choice == "Yes" else 0,
        "Type_of_material_cat_GRAVEL": 1 if material_choice == "GRAVEL" else 0,
        "Type_of_material_cat_NO_GRAVEL": 1 if material_choice == "NO_GRAVEL" else 0,
    }

# Fusionner les champs
fields = {"wearpart_type": wearpart_type, "static_input": static_input, **common_fields, **specific_fields}

# Bouton de soumission
if st.button("Prédire"):
    # Préparer les données pour le modèle
    model_input = pd.DataFrame([fields])
    try:
        # Obtenir une prédiction via l'endpoint
        prediction = score_model(model_input)
        st.success(f"Prédiction: {prediction}")
    except Exception as e:
        st.error(f"Erreur lors de la prédiction: {e}")

