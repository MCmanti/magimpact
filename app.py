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
        table_diameter = st.number_input("Table Diameter", value=0.0)
        design_flat = st.number_input("Design Flat", value=0.0)
        design_flat_2_layers = st.number_input("Design Flat - 2 Layers", value=0.0)
        design_pocket = st.number_input("Design Pocket", value=0.0)
        material_cat_gravel = st.number_input("Material Cat Gravel", value=0.0)

        inputs = [wearpart_type, "static_input_placeholder", tip_speed, table_diameter, flow_rate, abrasivity, density,
                  crushability, weight, df_90, df_50, df_10, dp_90, dp_50, dp_10, return_percentage, design_flat,
                  design_flat_2_layers, design_pocket, material_cat_gravel]

    elif wearpart_type == "Anvil":
        num_impellers = st.number_input("Number of Impellers", value=0.0)
        type_wear_part_qca_054 = st.number_input("Type Wear Part QCA-054", value=0.0)
        type_wear_part_qca_054h = st.number_input("Type Wear Part QCA-054H", value=0.0)
        ceramic_no = st.number_input("Ceramic No", value=0.0)
        ceramic_yes = st.number_input("Ceramic Yes", value=0.0)
        material_cat_gravel = st.number_input("Material Cat Gravel", value=0.0)
        material_cat_no_gravel = st.number_input("Material Cat No Gravel", value=0.0)

        inputs = [wearpart_type, "static_input_placeholder", tip_speed, num_impellers, flow_rate, abrasivity, density,
                  crushability, weight, df_90, df_50, df_10, dp_90, dp_50, dp_10, return_percentage,
                  type_wear_part_qca_054, type_wear_part_qca_054h, ceramic_no, ceramic_yes,
                  material_cat_gravel, material_cat_no_gravel]

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
                "Authorization": token
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
