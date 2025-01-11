import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import json

# Intégrer le token directement dans le code
os.environ["DATABRICKS_TOKEN"] = "dapie66246f9602999ec0960dda2b122efd3-3"  # Remplacez par votre token Databricks

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
static_input = st.sidebar.number_input("Average Wear Part Lifetime", value=0.0)

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

# Champs spécifiques à chaque type de pièce
if wearpart_type == "Impeller":
    specific_fields = {
        "Table Diameter": st.number_input("Table Diameter", value=0.0),
        "Design_Flat": st.checkbox("Design Flat", value=False),
        "Design_Flat - 2 layers": st.checkbox("Design Flat - 2 layers", value=False),
        "Design_Pocket": st.checkbox("Design Pocket", value=False),
        "Type_of_material_cat_GRAVEL": st.checkbox("Material Gravel", value=False),
    }
elif wearpart_type == "Anvil":
    specific_fields = {
        "Type of wear part_QCA-054": st.checkbox("Type QCA-054", value=False),
        "Type of wear part_QCA-054H": st.checkbox("Type QCA-054H", value=False),
        "Type of wear part_QCA-213": st.checkbox("Type QCA-213", value=False),
        "Type of wear part_QCA-218": st.checkbox("Type QCA-218", value=False),
        "Ceramic_No": st.checkbox("Ceramic No", value=False),
        "Ceramic_Yes": st.checkbox("Ceramic Yes", value=False),
        "Type_of_material_cat_GRAVEL": st.checkbox("Material Gravel", value=False),
        "Type_of_material_cat_NO_GRAVEL": st.checkbox("Material No Gravel", value=False),
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
