import streamlit as st

#config da página
st.set_page_config(
    page_title= "FSAE insights -> F1 Dashboard",
    page_icon= "🏎️",
    layout= "wide"
)

st.title("Análise de telemetria da F1 - GP de São Paulo | Insights para FSAE")
st.caption("Degaste dos pneus e performance")

#sidebar
ano = st.sidebar.selectbox("Temporada", [2024, 2023, 2022, 2021])
tipo_da_sessao = st.sidebar.radio(
    "Tipo de Sessão", 
    ["Qualificatória", "Corrida"],

)
st.sidebar.multiselect()

#Carregar dados

