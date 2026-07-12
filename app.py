import streamlit as st
from dados import load_session, get_laps, get_telemetry, clean_laps, clean_telemetry, feature_engineering
from graficos import plot_tempo_da_volta_por_piloto, plot_degradacao_pneu_por_composto, plot_velocidade_por_trecho, plot_distribuicao_de_velocidade, plot_taxa_de_degradacao_pneus

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
tipo_sessao = "Q" if "Q" in tipo_da_sessao else "R"

#Carregar dados
#Dados em cache do streamlit para evitar o reprocessamento dos dados
@st.cache_data(show_spinner="Carregando dados...")
def get_processed_data(ano, tipo_sessao):
    sessao = load_session(ano, tipo_sessao)
    voltas_sem_processamento = get_laps(sessao)
    voltas = clean_laps(voltas_sem_processamento)
    voltas = feature_engineering(voltas)
    return sessao, voltas

sessao, voltas = get_processed_data(ano, tipo_sessao)
 
#Filtrar dados por piloto
all_drivers = sorted(voltas["Driver"].unique().tolist())
piloto_selecionado = st.sidebar.multiselect("Pilotos", all_drivers, default=all_drivers[:5])

voltas_por_piloto = voltas[voltas["Driver"].isin(piloto_selecionado)]

#Indicadores gerais de performance da seção
st.subheader("Indicadores gerais da seção")
c1, c2, c3, c4 = st.columns(4)
tempo_mais_rapido = voltas.loc[voltas["LapTime_s"].idxmin()]
c1.metric("Volta mais rápida", f"{voltas['LapTime_s'].min():.3f}s")
c2.metric("Piloto mais rápido", tempo_mais_rapido["Driver"])
c3.metric("Composto mais usado", voltas["Compound"].value_counts().idxmax())
c4.metric("Total de Voltas Analisadas", len(voltas))

st.divider()

#Seção dos gráficos principais 
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.subheader("Evolução do Tempo por Volta")
    st.pyplot(plot_tempo_da_volta_por_piloto(voltas_por_piloto))

with coluna2:
    st.subheader("Degradação por Composto")
    st.pyplot(plot_degradacao_pneu_por_composto(voltas_por_piloto))

#Seção dos gráficos secudários
coluna3, coluna4 = st.columns(2)
with coluna3:
    st.subheader("Taxa Média de Degração ")
    st.pyplot(plot_taxa_de_degradacao_pneus(voltas_por_piloto))

with coluna4:
    st.subheader("Distribuição de Performance")
    st.bar_chart(voltas["PerformanceTier"].value_counts())

st.divider()

#Seção de telemetria
st.subheader("Telemetria Detalhada de Volta")
piloto_telemetria = st.selectbox("Selecione o Piloto", piloto_selecionado)

if piloto_telemetria:
    tempo_mais_rapido = voltas[voltas["Driver"] == piloto_telemetria].pick_fastest()
    telemetria_sem_processamento = get_telemetry(tempo_mais_rapido)

    if telemetria_sem_processamento is None:
        st.info("Selecione outro piloto ou ano para visualizar os gráficos.")

    telemetria = clean_telemetry(telemetria_sem_processamento)

    coluna5, coluna6 = st.columns(2)
    with coluna5:
        st.pyplot(plot_velocidade_por_trecho(telemetria))
    with coluna6:
        st.pyplot(plot_distribuicao_de_velocidade(telemetria))

st.divider()

st.subheader("Insights para a Equipe FSAE")
st.info(
    """ Texto dos insights"""
)
    




