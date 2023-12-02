import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.title("Envio de Cadasdro da AGIR para fornecedores")
st.markdown("Insira abaixo os dados para envio:")

conn = st.connection("gsheets", type=GSheetsConnection)


existing_data = conn.read(worksheet="fornecedores", usecols = list(range(6)), ttl=5)
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
    company_name = st.text_input(label="E-mail do destinatário*")
    business_type = st.text_input(label="E-mail do remetente*")
    unidade = st.multiselect("Unidade a ser cadastrada:*", options=unidade)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not company_name or not business_type or not unidade:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        elif existing_data["destinatario"].str.contains(company_name).any():
            st.warning("A vendor with this company name already exists.")
            st.stop()
        else:
            # Create a new row of vendor data
            vendor_data = pd.DataFrame(
                [
                    {
                        "destinatario": company_name,
                        "remetente": business_type,
                        "unidade": ", ".join(unidade),
                        "YearsInBusiness": years_in_business,
                        "OnboardingDate": onboarding_date.strftime("%Y-%m-%d"),
                        "AdditionalInfo": additional_info,
                    }
                ]
            )

            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)

            # Update Google Sheets with the new vendor data
            conn.update(worksheet="fornecedores", data=updated_df)

            st.success("Vendor details successfully submitted!")
