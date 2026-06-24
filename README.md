### Análise de Dados da Fórmula 1 aplicada à Fórmula SAE — GP São Paulo

> Projeto desenvolvido para a disciplina de Novas Tecnologias — Engenharia de Software  
> Stack: Python · FastF1 · Pandas · Numpy · Matplotlib · Streamlit

---

## 📌 Sobre o Projeto

Este projeto analisa dados de telemetria e performance dos carros de Fórmula 1 no **Grande Prêmio de São Paulo**, com o objetivo de extrair insights aerodinâmicos e de desgaste de pneus aplicáveis ao desenvolvimento de um carro da **Fórmula SAE (FSAE)**.

A interface interativa permite explorar tempos de volta, degradação de pneus por compound, mapas de velocidade na pista e comparativos entre pilotos.

---

## 📁 Estrutura do Projeto

```
projeto_f1/
├── app.py               # Interface Streamlit (ponto de entrada)
├── dados.py             # Coleta de dados via FastF1 API, limpeza e feature engineering (Pandas + Numpy)
├── graficos.py          # Visualizações com Matplotlib
├── cache/               # Cache automático do FastF1 (gerado na 1ª execução)
├── requirements.txt     # Dependências do projeto
└── README.md            # Este arquivo
```

---

## ⚙️ Pré-requisitos

- **Python** 3.10 ou superior
- **pip** atualizado
- Conexão com a internet na **primeira execução** (para baixar os dados da FastF1)

---

## 🚀 Instalação e Execução

### 1. Clone o repositório ou extraia os arquivos

```bash
# Via git
git clone https://github.com/seu-usuario/projeto-f1-fsae.git
cd projeto-f1-fsae

# Ou simplesmente extraia o ZIP e entre na pasta
cd projeto_f1
```

### 2. (Recomendado) Crie um ambiente virtual

```bash
# Criar ambiente
python -m venv venv

# Ativar — Windows
venv\Scripts\activate

# Ativar — Linux / macOS
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`.

> ⏳ **Primeira execução:** o FastF1 irá baixar os dados do GP São Paulo e armazená-los na pasta `cache/`. Isso pode levar alguns minutos dependendo da conexão. As execuções seguintes serão instantâneas.

---

## 📦 Dependências

| Biblioteca | Versão Mínima | Finalidade |
|---|---|---|
| `fastf1` | 3.3.0 | Acesso à API de dados da Fórmula 1 |
| `pandas` | 2.0.0 | Manipulação e limpeza de dados tabulares |
| `numpy` | 1.26.0 | Cálculos numéricos, regressão linear, normalização |
| `matplotlib` | 3.8.0 | Geração de gráficos e visualizações |
| `streamlit` | 1.35.0 | Interface web interativa |

Arquivo `requirements.txt`:

```
fastf1>=3.3.0
pandas>=2.0.0
numpy>=1.26.0
matplotlib>=3.8.0
streamlit>=1.35.0
```

---

## 🖥️ Funcionalidades da Interface

### Painel lateral (sidebar)
- **Temporada** — selecione entre 2022, 2023 ou 2024
- **Tipo de sessão** — Qualificatória (performance pura) ou Corrida (estratégia de pneus)
- **Filtro de pilotos** — selecione quais pilotos incluir na análise

### Seção principal
| Painel | Descrição |
|---|---|
| 📊 Indicadores Gerais | Volta mais rápida, piloto destaque, compound mais usado |
| ⏱️ Evolução por Volta | Linha do tempo dos tempos de cada piloto |
| 🔴 Degradação por Compound | Dispersão + linha de tendência (regressão linear) por tipo de pneu |
| 📉 Taxa Média de Degradação | Comparativo em barras: segundos perdidos por volta por compound |
| 🗺️ Mapa de Velocidade | Visualização da pista colorida por velocidade (telemetria) |
| 📦 Distribuição de Performance | Categorização das voltas por quartil (Elite / Boa / Regular / Lenta) |
| 💡 Insights FSAE | Conclusões aplicadas às provas da Fórmula SAE |

---

## 🔬 Features Criadas (Engenharia de Dados)

| Feature | Origem | Método |
|---|---|---|
| `LapTime_s` | conversão de `timedelta` | `dt.total_seconds()` + `np.float64` |
| `DeltaToBest_pct` | diferença percentual para a melhor volta | divisão vetorizada com `numpy` |
| `TyreDegRate` | taxa de desgaste do pneu por volta | `np.polyfit` (regressão linear) |
| `LapTime_norm` | normalização 0–1 do tempo de volta | normalização min-max com `numpy` |
| `PerformanceTier` | classificação por quartil | `pd.qcut` com 4 categorias |

---

## 🗂️ Fonte dos Dados

- **FastF1 API** — biblioteca Python que acessa a base [Ergast F1](http://ergast.com/mrd/) e os dados oficiais de telemetria da F1
- **Grande Prêmio escolhido:** São Paulo (Interlagos)
- **Motivo da escolha:** proximidade com o Centro de Testes Ford em Tatuí/SP, local das provas da FSAE

---

## ⚠️ Possíveis Erros e Soluções

| Erro | Causa | Solução |
|---|---|---|
| `ModuleNotFoundError` | dependência não instalada | rode `pip install -r requirements.txt` novamente |
| `SessionNotAvailableError` | dados não disponíveis para o ano/GP | tente outro ano (2023 ou 2024) |
| Gráfico em branco | nenhum piloto selecionado no filtro | selecione ao menos um piloto na sidebar |
| Lentidão na 1ª execução | download dos dados da FastF1 | aguarde; execuções seguintes usam o cache |

---

## 📚 Referências

- [FastF1 — Documentação oficial](https://docs.fastf1.dev/)
- [Ergast F1 API](http://ergast.com/mrd/)
- [Formula 1 — Guia de pneus](https://www.formula1.com/en/latest/article/the-beginners-guide-to-f1-tyres.61SvF0Kfg29UR2SPhakDqd)
- [Streamlit — Documentação](https://docs.streamlit.io/)
- FSAE Unicamp — Regulamento de Provas Dinâmicas
