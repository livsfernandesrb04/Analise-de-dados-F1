import streamlit as st
from dados import load_session, get_laps, get_telemetry, clean_laps, clean_telemetry
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
@st.cache_data(show_spinner="Carregando dados...")
def get_data(ano, ):
    session = load_session(ano, )
    voltas

#Indicadores gerais de performance da seção
st.subheader("Indicadores gerais da seção")
c1, c2, c3, c4 = st.columns(4)

#Seção dos gráficos principais 
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.subheader("Evolução do Tempo por Volta")
    st.pyplot()

with coluna2:
    st.subheader("Degradação por Composto")
    st.pyplot()

#Seção dos gráficos secudários
coluna3, coluna4 = st.columns(2)
with coluna3:
    st.subheader("Taxa Média de Degração ")
    st.pyplot()

with coluna4:
    st.subheader("Distribuição de Performance")
    st.pyplot()

#Seção de telemetria





