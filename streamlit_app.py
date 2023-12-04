import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.title("Envio de Cadastro da AGIR para fornecedores 📤")
st.markdown("Insira abaixo os dados para envio:")

conn = st.connection("gsheets", type=GSheetsConnection)


existing_data = conn.read(worksheet="fornecedores", usecols = list(range(3)), ttl=2)
existing_data = existing_data.dropna(how="all")



unidade = [
    "AGIR",
    "CRER",
    "HDS",
    "HUGOL",
    "CED",
    "TEIA",
    "HECAD"
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    destinatario_name = st.text_input(label="E-mail do destinatário*")
    business_type = st.text_input(label="E-mail do remetente*")
    unidade = st.multiselect("Unidade a ser cadastrada:*", options=unidade)
    

    # Mark mandatory fields
    st.markdown("**Campo obrigatório*")

    submit_button = st.form_submit_button(label="Enviar cadastro para o fornecedor")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not destinatario_name or not business_type or not unidade:
            st.warning("Não enviado. Algum dos campos obrigatórios foi preenchido.")
            st.stop()
       
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "destinatario": destinatario_name,
                        "remetente": business_type,
                        "unidade": ", ".join(unidade),
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="fornecedores", data=updated_df)

            st.success("Informações para cadastro enviadas com sucesso ao fornecedor!")
