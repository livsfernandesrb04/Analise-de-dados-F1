import pandas as pd
import numpy as np
import fastf1

#enable cache
fastf1.Cache.enable_cache('cache/')

#load session
def load_session( ano: int, tipo_da_sessao: str):
    session = fastf1.get_session(ano, "São Paulo", tipo_da_sessao)
    session.load()
    return session

#get the laps
def get_laps(session) -> pd.DataFrame:
    voltas = session.get_laps
    return voltas

#get the telemetry
def get_telemetry(lap) -> pd.DataFrame:
    dados_da_volta = lap.get_telemetry().add_distance()
    return dados_da_volta


#--------- Limpeza do dados -----------

#Remover dados inválidos
#clean laps
def clean_laps(voltas: pd.DataFrame) -> pd.DataFrame:
    voltas = voltas[voltas["PitOutTime"].isna() & voltas["PitInTime"].isna()].copy()
    voltas = laps.drop_duplicates(subset=["Driver", "LapNumber"])
    voltas = voltas.fill_missing()
    voltas["LapTime_seconds"] = voltas["LapTime"].dt.total_seconds().astype(np.float64)

    return voltas 

#clean telemetry
def clean_telemetry(telemetria: pd.DataFrame) -> pd.DataFrame:
    telemetria = telemetria.ffill().bfill()
    telemetria = telemetria[telemetria["Speed"]. between(0, 400)]
    telemetria["Normalized_speed"] = (telemetria["Speed"] - telemetria["Speed"].min()/ telemetria["Speed"].max() - telemetria["Speed"].min())
    return telemetria

#Feature Engineering
def feature_engineering(voltas: pd.DataFrame) -> pd.DataFrame:
    #Delta percentual em relação a volta mais rápida
    #Taxa de degração do pneu por piloto e composto
    def calcular_desgaste():
    
    #Normalização do tempo de volta para comparar entre os pilotos
    #Classificação da volta de acordo com a performance
    
