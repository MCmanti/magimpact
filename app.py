import streamlit as st
import requests
import json

def main():
    st.title("Application de Prédiction de Wear Parts")
    st.write("Saisissez les entrées pour obtenir une prédiction du modèle.")

    # Sélection du type de wear part
    wearpart_type = st.selectbox("Type de Wear Part", ["Impeller", "Anvil"])

    # Entrées communes
    tip_speed = st.number_input("Tip Speed", value=0.0)
    flow_rate = st.number_input("Flow Rate", value=0.0)
    abrasivity = st.number_input("Abrasivity", value=0.0)
    density = st.number_input("Density", value=0.0)
    crushability = st.number_input("Crushability", value=0.0)
    weight = st.number_input("Weight", value=0.0)
    df_90 = st.number_input("DF 90", value=0.0)
    df_50 = st.number_input("DF 50", value=0.0)
    df_10 = st.number_input("DF 10", value=0.0)
    dp_90 = st.number_input("DP 90", value=0.0)
    dp_50 = st.number_input("DP 50", value=0.0)
    dp_10 = st.number_input("DP 10", value=0.0)
    return_percentage = st.number_input("Return Percentage", value=0.0)

    # Entrées spécifiques
    if wearpart_type == "Impeller":
        # Listes déroulantes pour Design et Material
        design_choice = st.selectbox("Select Design", ["None", "Flat", "Flat - 2 layers", "Pocket"])
        material_choice = st.selectbox("Select Material", ["None", "GRAVEL"])

        # Gestion des valeurs spécifiques
        design_flat = 1 if design_choice == "Flat" else 0
        design_flat_2_layers = 1 if design_choice == "Flat - 2 layers" else 0
        design_pocket = 1 if design_choice == "Pocket" else 0
        material_cat_gravel = 1 if material_choice == "GRAVEL" else 0

        # Autres entrées spécifiques
        table_diameter = st.number_input("Table Diameter", value=0.0)

        inputs = [
            wearpart_type, "static_input_placeholder", tip_speed, table_diameter, flow_rate, abrasivity, density,
            crushability, weight, df_90, df_50, df_10, dp_90, dp_50, dp_10, return_percentage, design_flat,
            design_flat_2_layers, design_pocket, material_cat_gravel
        ]

    elif wearpart_type == "Anvil":
        # Listes déroulantes pour Type of Wear Part, Ceramic, and Material
        wearpart_choice = st.selectbox("Select Wear Part", ["None", "QCA-054", "QCA-054H", "QCA-213", "QCA-218"])
        ceramic_choice = st.selectbox("Select Ceramic", ["None", "Yes", "No"])
        material_choice = st.selectbox("Select Material", ["None", "GRAVEL", "NO_GRAVEL"])

        # Gestion des valeurs spécifiques
        type_wear_part_qca_054 = 1 if wearpart_choice == "QCA-054" else 0
        type_wear_part_qca_054h = 1 if wearpart_choice == "QCA-054H" else 0
        type_wear_part_qca_213 = 1 if wearpart_choice == "QCA-213" else 0
        type_wear_part_qca_218 = 1 if wearpart_choice == "QCA-218" else 0
        ceramic_no = 1 if ceramic_choice == "No" else 0
        ceramic_yes = 1 if ceramic_choice == "Yes" else 0
        material_cat_gravel = 1 if material_choice == "GRAVEL" else 0
        material_cat_no_gravel = 1 if material_choice == "NO_GRAVEL" else 0

        # Autres entrées spécifiques
        num_impellers = st.number_input("Number of Impellers", value=0.0)

        inputs = [
            wearpart_type, "static_input_placeholder", tip_speed, num_impellers, flow_rate, abrasivity, density,
            crushability, weight, df_90, df_50, df_10, dp_90, dp_50, dp_10, return_percentage,
            type_wear_part_qca_054, type_wear_part_qca_054h, type_wear_part_qca_213, type_wear_part_qca_218,
            ceramic_no, ceramic_yes, material_cat_gravel, material_cat_no_gravel
        ]

    # Bouton pour envoyer la requête
    if st.button("Obtenir la Prédiction"):
        try:
            # Construire la requête JSON
            request_body = json.dumps({"inputs": inputs})

            # URL de l'API
            api_url = "https://adb-4282284702815533.13.azuredatabricks.net/serving-endpoints/magimpact/invocations"

            # Token d'authentification
            token = "dapic18ea4067f8260fc6a71cbcc86748a0d-3"

            # Envoyer la requête POST
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}" 
            }
            response = requests.post(api_url, data=request_body, headers=headers)

            # Traiter la réponse
            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Prédiction réussie : {prediction}")
            else:
                st.error(f"Erreur lors de la requête : {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()
