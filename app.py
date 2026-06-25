import streamlit as st
from dados import
from graficos import 

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
Piloto = st.sidebar.multiselect("Pilotos",[] )

#Carregar dados
#Dados em cache do streamlit para evitar o reprocessamento dos dados


#Seção dos gráficos principais 
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.subheader("Evolução do Tempo por Volta")
    st.pyplot()

with coluna2:
    st.subheader("Degradação por Composto")
    st

#Seção dos gráficos secudários
coluna3, coluna4 = st.columns(2)
with coluna3:
    st.subheader("Taxa Média de Degração ")

with coluna4:
    st.subheader("Distribuição de Performance")

#Seção de telemetria





