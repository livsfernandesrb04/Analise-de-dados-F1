import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import numpy as np
from numpy.polynomial import Polynomial

#Plotar os tempos de cada lap
def plot_tempo_da_volta_por_piloto(voltas):
    fig, ax = plt.subplots(figsize=(10, 6))

    for driver in voltas["Driver"].unique():
       d = voltas[voltas["Driver"] == driver]
       ax.plot(d["LapNumber"], d["LapTime_s"], marker="o", markersize=3, label=driver)

    ax.set(
       title="Evolução do Tempo por Volta - GP São Paulo",
       xlabel="Número da Volta",
       ylabel="Tempo da Volta (em seg)"
    )
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.5)
    return fig


#Plotar a degradação dos pneus por composto
def plot_degradacao_pneu_por_composto(voltas):
    cores_composto = {"SOFT": "red", "MEDIUM": "yellow", "HARD": "white", "WET": "blue", "INTERMEDIATE": "green"}
    fig, ax = plt.subplots(figsize=(10, 5))

    for composto, grupo in voltas.groupby("Compound"):
       color = cores_composto.get(composto, "purple")
       ax.scatter(grupo["TyreLife"], grupo["LapTime_s"], label=composto, color=color, alpha=0.5, s=20)

    if len(grupo) >= 3:
       z = Polynomial.fit(grupo["TyreLife"], grupo["LapTime_s"], 1)
       x_range = np.linspace(grupo["TyreLife"].min(), grupo["TyreLife"].max(), 100)
       ax.plot(x_range, z(x_range), color=color, linewidth=2.5)

    
    ax.set(
       title="Degradação de Pneu por Composto - GP São Paulo",
       xlabel="Voltas com o Pneu",
       ylabel="Tempo da Volta (em seg)"
    )
    ax.legend(title="Composto")
    ax.grid(True, linestyle="--", alpha=0.4)
    return fig

#Plotar a velocidade em cada trecho do mapa
def plot_velocidade_por_trecho(telemetria):
   fig, ax = plt.subplots(figsize=(8, 8))
   sc = ax.scatter(telemetria["X"], telemetria["Y"], c=telemetria["Speed"], cmap="RdY1Gn", s=2, alpha=0.8)
   cbar = plt.colorbar(sc, ax=ax)
   cbar.set_label("Velocidade (Km/h)")

   ax.set(
      title="Velocidade por Trecho - GP São Paulo",
      xlabel="Posição X(m)",
      ylabel="Posição Y(m)"
   )

   ax.axis("equal")
   return fig

#Plotar a distribuição da velocidade
def plot_distribuicao_de_velocidade(telemetria):
   fig, ax = plt.subplots(figsize=(8, 5))
   ax.hist(telemetria["Speed"], bins=60, color="steelblue", edgecolor="black", alpha=0.8)
   ax.axvline(
      telemetria["Speed"].mean(), 
      color="red", 
      linestyle="--", 
      label=f"Média: {telemetria["Speed"].mean():.1f} km/h"
    )
   
   ax.set(
      title="Distribuição de Velocidade no mapa",
      xlabel="Velocidade (km/h)",
      ylabel="Frequência"
   )
   ax.grid(True, linestyle="--", alpha=0.4)
   return fig

#Plotar a taxa de degradação dos pneu por composto
def plot_taxa_de_degradacao_pneus(voltas):
   degradacao = voltas.groupby("Compound")["TyreDegradationRate"].mean().dropna()
   fig, ax = plt.subplots(figsize=(6, 4))
   bars = ax.bar(degradacao.index, degradacao.values, color=["white", "yellow", "red"][:len(degradacao)])

   ax.bar_label(bars, fmt="%.4f", padding=3)

   ax.set(
      title="Taxa média de Desgaste por Tipo de Pneu",
      xlabel="Composto",
      ylabel="Degradação Média (s/volta)"
   )
   ax.grid(True, axis="y",linestyle="--", alpha=0.4)
   return fig
