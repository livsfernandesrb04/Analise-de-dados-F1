import streamlit as st
import pandas as pd
import numpy as np
import fastf1

#enable cache
fastf1.Cache.enable_cache('cache/')

#load session
def load_session( ano: int, tipo_da_sessao: str):
    session = fastf1.get_session(ano, "São Paulo", tipo_da_sessao)
    session.load(telemetry=True)
    return session

#get the laps
def get_laps(session) -> pd.DataFrame:
    voltas = session.laps
    return voltas

#get the telemetry
def get_telemetry(lap) -> pd.DataFrame:
    #Indicar erro caso os dados não existam
    try:
        return lap.get_telemetry().add_distance()
    
    except AttributeError as e:
        st.warning("Os dados de telemetria não estão disponíveis nessa sessão.")
    except KeyError as e:
        st.warning("Telemetria não encontrada para o piloto escolhido.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao carregar a telemetria: {e}")
        return None



#--------- Limpeza do dados -----------

#Remover dados inválidos
#Clean laps -> Remover voltas inválidas e tratar valores ausentes.
def clean_laps(voltas: pd.DataFrame) -> pd.DataFrame:
    #Remover voltas com pit stop
    voltas = voltas[voltas["PitOutTime"].isna() & voltas["PitInTime"].isna()].copy()

    #Remover duplicatas
    voltas = voltas.drop_duplicates(subset=["Driver", "LapNumber"])

    #Tratar nulos
    voltas = voltas.dropna(subset=["LapTime", "Compound", "TyreLife"])

    #Conversão de tipo: LapTime (timedelta) -> segundos (float)
    voltas["LapTime_s"] = voltas["LapTime"].dt.total_seconds().astype(np.float64)

    return voltas 

#clean telemetry -> Limpar e normalizar os dados de telemetria
def clean_telemetry(telemetria: pd.DataFrame) -> pd.DataFrame:
    #Preencher dados que faltam  
    telemetria = telemetria.ffill().bfill()

    #Normalizar a velocidade
    telemetria = telemetria[telemetria["Speed"]. between(0, 400)]
    telemetria["Normalized_speed"] = (telemetria["Speed"] - telemetria["Speed"].min())/ (telemetria["Speed"].max() - telemetria["Speed"].min())
    
    return telemetria

#Feature Engineering
def feature_engineering(voltas: pd.DataFrame) -> pd.DataFrame:
    #Delta percentual em relação a volta mais rápida
    melhor_tempo = voltas["LapTime_s"].min()
    voltas["DeltaPercetual_EmRelacaoAoMelhorTempo"] = np.round(((voltas["LapTime_s"] - melhor_tempo) / melhor_tempo) * 100, 3)

    #Taxa de degração do pneu por piloto e composto
    def calcular_taxa_desgaste(grupo):
        if len(grupo) < 3:
            grupo["TyreDegradationRate"] = np.nan
            return grupo
        coeficientes = np.polyfit(grupo["TyreLife"], grupo["LapTime_s"], deg=1)
        grupo["TyreDegradationRate"] = coeficientes[0]
        return grupo

    voltas = voltas.groupby(["Driver", "Compound"], group_keys=False).apply(calcular_taxa_desgaste)

    #Normalização do tempo de volta para comparar entre os pilotos
    min_t = voltas["LapTime_s"].min()
    max_t = voltas["LapTime_s"].max()
    voltas["LapTime_normalizado"] = (voltas["LapTime_s"] - min_t) / (max_t - min_t)

    #Classificação da volta de acordo com a performance
    voltas["PerformanceTier"] = pd.qcut(
        voltas["LapTime_s"], q=4,
        labels=["Ótima","Boa","Regular","Lenta"]
    )

    return voltas
    
