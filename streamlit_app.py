import streamlit as st
import requests
import json

def main():
    st.title("Modèle de prédiction pour les pièces d'usure du MagImpact")
    st.write("Saisissez les entrées pour obtenir une prédiction du modèle.")

    # --- COLONNES : col1 (caractéristique de la pièce) vs col2 (restes des inputs) ---
    col1, col2 = st.columns([1, 3])

    # =======================
    # 1) Caractéristiques de la pièce (col1, côté gauche)
    # =======================
    with col1:
        st.markdown("### Caractéristiques de la pièce")

        # 1.a) Sélection du type de Wear Part
        wearpart_type = st.selectbox("Type de Wear Part", ["Impeller", "Anvil"])

        # 1.b) Weight (commun aux deux, dans vos specs)
        weight = st.number_input("Weight", value=0.0)

        # 1.c) Variables spécifiques selon wearpart_type
        if wearpart_type == "Impeller":
            # Design
            design_choice = st.selectbox("Select Design", ["None", "Flat", "Flat - 2 layers", "Pocket"])
            # Material (GRAVEL ou None)
            material_choice = st.selectbox("Select Material", ["None", "GRAVEL"])

            # Conversion en variables binaires (design/material)
            design_flat = 1 if design_choice == "Flat" else 0
            design_flat_2_layers = 1 if design_choice == "Flat - 2 layers" else 0
            design_pocket = 1 if design_choice == "Pocket" else 0
            material_cat_gravel = 1 if material_choice == "GRAVEL" else 0

            # (On stocke temporairement ces variables dans un dictionnaire ou des variables locales ;
            #  on les utilisera plus bas dans la construction finale de 'inputs'.)

            # On s'en souviendra dans un dictionnaire :
            piece_caracs = {
                "design_flat": design_flat,
                "design_flat_2_layers": design_flat_2_layers,
                "design_pocket": design_pocket,
                "material_cat_gravel": material_cat_gravel
            }

            # On mettra "weight" dans la liste finale à la même position qu'avant.

        elif wearpart_type == "Anvil":
            # Type of Wear Part
            wearpart_choice = st.selectbox("Select Wear Part", ["None", "QCA-054", "QCA-054H", "QCA-213", "QCA-218"])
            # Ceramic
            ceramic_choice = st.selectbox("Select Ceramic", ["None", "Yes", "No"])
            # Material (GRAVEL, NO_GRAVEL, None)
            material_choice = st.selectbox("Select Material", ["None", "GRAVEL", "NO_GRAVEL"])

            # Conversion en variables binaires
            type_wear_part_qca_054 = 1 if wearpart_choice == "QCA-054" else 0
            type_wear_part_qca_054h = 1 if wearpart_choice == "QCA-054H" else 0
            type_wear_part_qca_213 = 1 if wearpart_choice == "QCA-213" else 0
            type_wear_part_qca_218 = 1 if wearpart_choice == "QCA-218" else 0
            ceramic_no = 1 if ceramic_choice == "No" else 0
            ceramic_yes = 1 if ceramic_choice == "Yes" else 0
            material_cat_gravel = 1 if material_choice == "GRAVEL" else 0
            material_cat_no_gravel = 1 if material_choice == "NO_GRAVEL" else 0

            # On stocke dans un dictionnaire :
            piece_caracs = {
                "type_wear_part_qca_054": type_wear_part_qca_054,
                "type_wear_part_qca_054h": type_wear_part_qca_054h,
                "type_wear_part_qca_213": type_wear_part_qca_213,
                "type_wear_part_qca_218": type_wear_part_qca_218,
                "ceramic_no": ceramic_no,
                "ceramic_yes": ceramic_yes,
                "material_cat_gravel": material_cat_gravel,
                "material_cat_no_gravel": material_cat_no_gravel
            }

    # =======================
    # 2) Autres inputs (col2, côté droit)
    # =======================
    with col2:
        st.markdown("### Autres paramètres")

        # On peut les regrouper dans des expanders pour faire plus propre.
        with st.expander("Caractéristiques Mécaniques"):
            tip_speed = st.number_input("Tip Speed", value=0.0)
            flow_rate = st.number_input("Flow Rate", value=0.0)
            abrasivity = st.number_input("Abrasivity", value=0.0)
            crushability = st.number_input("Crushability", value=0.0)

        with st.expander("Caractéristiques Physiques"):
            density = st.number_input("Density", value=0.0)
            # weight est déjà dans col1
            # => on n'affiche pas ici, on l'a mis dans la colonne de gauche

        with st.expander("Granulométrie (DF / DP)"):
            df_90 = st.number_input("DF 90", value=0.0)
            df_50 = st.number_input("DF 50", value=0.0)
            df_10 = st.number_input("DF 10", value=0.0)
            dp_90 = st.number_input("DP 90", value=0.0)
            dp_50 = st.number_input("DP 50", value=0.0)
            dp_10 = st.number_input("DP 10", value=0.0)

        with st.expander("Autres"):
            return_percentage = st.number_input("Return Percentage", value=0.0)

        # Paramètres spécifiques restants
        if wearpart_type == "Impeller":
            st.markdown("#### Paramètre Impeller : Table Diameter")
            table_diameter = st.number_input("Table Diameter", value=0.0)

        elif wearpart_type == "Anvil":
            st.markdown("#### Paramètre Anvil : Number of Impellers")
            num_impellers = st.number_input("Number of Impellers", value=0.0)

    # =======================
    # 3) Construire la liste 'inputs' en conservant l'ordre exact d'origine
    # =======================
    if wearpart_type == "Impeller":
        # On récupère les variables binaires dans piece_caracs
        design_flat              = piece_caracs["design_flat"]
        design_flat_2_layers     = piece_caracs["design_flat_2_layers"]
        design_pocket            = piece_caracs["design_pocket"]
        material_cat_gravel      = piece_caracs["material_cat_gravel"]

        # => On reconstruit la liste EXACTEMENT comme avant
        inputs = [
            wearpart_type,
            "Averge wear part lifetime",
            tip_speed,
            table_diameter,
            flow_rate,
            abrasivity,
            density,
            crushability,
            weight,            # on a récupéré plus haut dans col1
            df_90,
            df_50,
            df_10,
            dp_90,
            dp_50,
            dp_10,
            return_percentage,
            design_flat,
            design_flat_2_layers,
            design_pocket,
            material_cat_gravel
        ]

    else:  # wearpart_type == "Anvil"
        type_wear_part_qca_054    = piece_caracs["type_wear_part_qca_054"]
        type_wear_part_qca_054h   = piece_caracs["type_wear_part_qca_054h"]
        type_wear_part_qca_213    = piece_caracs["type_wear_part_qca_213"]
        type_wear_part_qca_218    = piece_caracs["type_wear_part_qca_218"]
        ceramic_no                = piece_caracs["ceramic_no"]
        ceramic_yes               = piece_caracs["ceramic_yes"]
        material_cat_gravel       = piece_caracs["material_cat_gravel"]
        material_cat_no_gravel    = piece_caracs["material_cat_no_gravel"]

        inputs = [
            wearpart_type, 
            "Averge lifetime wear part", 
            tip_speed, 
            num_impellers, 
            flow_rate, 
            abrasivity, 
            density,
            crushability, 
            weight,        # note : dans col1
            df_90, 
            df_50, 
            df_10, 
            dp_90, 
            dp_50, 
            dp_10, 
            return_percentage,
            type_wear_part_qca_054, 
            type_wear_part_qca_054h, 
            type_wear_part_qca_213, 
            type_wear_part_qca_218,
            ceramic_no, 
            ceramic_yes, 
            material_cat_gravel, 
            material_cat_no_gravel
        ]

    # =======================
    # 4) Bouton pour la prédiction
    # =======================
    st.markdown("---")
    if st.button("Obtenir la Prédiction"):
        try:
            # Construire la requête JSON
            request_body = json.dumps({"inputs": inputs})

            # URL de l'API (à adapter)
            api_url = "https://adb-4282284702815533.13.azuredatabricks.net/serving-endpoints/magimpact3/invocations"

            # Token d'authentification (à adapter)
            token = "dapic18ea4067f8260fc6a71cbcc86748a0d-3"

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            response = requests.post(api_url, data=request_body, headers=headers)

            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Prédiction réussie : {prediction}")
            else:
                st.error(f"Erreur lors de la requête : {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    main()


