import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


st.title("Envio de Cadasdro da AGIR para fornecedores")
st.markdown("Insira abaixo os dados para envio:")

conn = st.connection("gsheets", type=GSheetsConnection)


existing_data = conn.read(worksheet="fornecedores", usecols = list(range(6)), ttl=5)
existing_data = existing_data.dropna(how="all")

st.dataframe(existing_data)
