import streamlit as st
st.set_page_config(page_title="SentinelaMSF Yanomami", layout="wide")
import pandas as pd
from sentinela.db import SessionLocal, AlertaINMET, MalariaCaso, EnchenteDetectada, PredicaoRisco
import folium
from streamlit_folium import st_folium
import os
import requests
from dotenv import load_dotenv

st.title("SentinelaMSF Yanomami: Monitoramento de Riscos")

# Carrega a chave da Weather API do .env (ajuste o caminho se necessário)
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def get_weather(city):
    """
    Consulta a Weather API e retorna um dicionário com as condições climáticas atuais da cidade.
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&lang=pt"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "condicao": data["current"]["condition"]["text"],
                "temp_c": data["current"]["temp_c"],
                "umidade": data["current"]["humidity"],
                "vento_kph": data["current"]["wind_kph"]
            }
        else:
            return None
    except Exception:
        return None

# Funções utilitárias para consulta ao banco
def get_alertas():
    db = SessionLocal()
    alertas = db.query(AlertaINMET).order_by(AlertaINMET.data_emissao.desc()).all()
    db.close()
    return alertas

def get_predicoes():
    db = SessionLocal()
    predicoes = db.query(PredicaoRisco).order_by(PredicaoRisco.score.desc()).all()
    db.close()
    return predicoes

def get_malaria_casos():
    db = SessionLocal()
    casos = db.query(MalariaCaso).all()
    db.close()
    return casos

def get_enchentes():
    db = SessionLocal()
    enchentes = db.query(EnchenteDetectada).all()
    db.close()
    return enchentes

# Sidebar para filtros
st.sidebar.header("Filtros de Risco")
st.sidebar.markdown("""
Selecione o nível de risco para filtrar as predições exibidas. 
- **Alto**: Municípios com risco elevado de eventos críticos.
- **Médio**: Atenção moderada.
- **Baixo**: Situação controlada.
""")
risco_filter = st.sidebar.selectbox("Nível de Risco", ["Todos", "alto", "medio", "baixo"], help="Filtre as predições de risco exibidas na tabela e no mapa.")

# Botão para atualizar alertas
if st.sidebar.button("Atualizar Alertas Climáticos"):
    from sentinela.ingest_weather import ingest_weather_alerts
    ingest_weather_alerts()
    st.sidebar.success("Alertas atualizados!")
    st.sidebar.info("Os dados são obtidos da WeatherAPI e salvos localmente.")

# Exibir alertas recentes
st.subheader("Últimos Alertas Climáticos 🛰️")
st.markdown("""
Os alertas abaixo são provenientes da WeatherAPI/INMET e representam eventos climáticos críticos recentes para a região monitorada.
""")
alertas = get_alertas()
if alertas:
    for alerta in alertas[:5]:
        st.warning(f"<span style='font-size:16px;'>{alerta.data_emissao.strftime('%d/%m/%Y %H:%M')}</span> <b>{alerta.tipo}</b> - <b>{alerta.regiao}</b><br>{alerta.descricao}", icon="⚠️", unsafe_allow_html=True)
else:
    st.info("Nenhum alerta recente disponível.")

# Exibir estatísticas rápidas
st.subheader("Estatísticas de Risco 📊")
st.markdown("""
A tabela mostra os 5 municípios atualmente com maior risco, segundo o modelo de predição. O score indica a intensidade do risco.
""")
predicoes = get_predicoes()
if predicoes:
    df_pred = pd.DataFrame([{ 'Município': p.municipio, 'Risco': p.risco, 'Score': p.score, 'Fatores': getattr(p, 'fatores', 'N/A') } for p in predicoes])
    if risco_filter != "Todos":
        df_pred = df_pred[df_pred['Risco'] == risco_filter]
    top5 = df_pred.sort_values('Score', ascending=False).head(5)
    st.table(top5)
else:
    st.info("Sem predições de risco disponíveis.")

# Mapa interativo
st.subheader("Mapa de Risco e Enchentes 🗺️")
st.markdown("""
No mapa abaixo, marcadores <span style='color:red'><b>vermelhos</b></span> indicam municípios com risco ALTO, e círculos <span style='color:blue'><b>azuis</b></span> indicam enchentes detectadas. Passe o mouse sobre os marcadores para detalhes.
"", unsafe_allow_html=True)
mapa = folium.Map(location=[-0.5, -64.5], zoom_start=6)

# Adicionar marcadores de enchentes
enchentes = get_enchentes()
for ench in enchentes:
    folium.CircleMarker(
        location=[-0.5, -64.5],  # Ajustar para coordenadas reais se disponíveis
        radius=8,
        popup=f"{ench.municipio} ({ench.data.strftime('%d/%m/%Y')}): {ench.area_alagada_km2} km²",
        color="blue",
        fill=True,
        fill_color="blue"
    ).add_to(mapa)

# Adicionar marcadores de risco alto
for p in predicoes:
    if p.risco == "alto":
        fatores = getattr(p, 'fatores', None)
        popup_text = f"{p.municipio}: <b>Risco ALTO</b> ({p.score:.2f})"
        if fatores:
            popup_text += f"<br><i>Fatores: {fatores}</i>"
        folium.Marker(
            location=[-0.5, -64.5],  # Ajustar para coordenadas reais se disponíveis
            popup=popup_text,
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(mapa)

st_folium(mapa, width=900, height=500)

# Evolução dos casos de malária
st.subheader("Evolução dos Casos de Malária 🦟")
st.markdown("""
A linha abaixo mostra a evolução temporal do número de casos de malária reportados na base histórica.
""")
casos = get_malaria_casos()
if casos:
    df_casos = pd.DataFrame([{ 'Município': c.municipio, 'Data': c.data, 'Casos': c.casos } for c in casos])
    st.line_chart(df_casos.groupby('Data')['Casos'].sum())
else:
    st.info("Sem dados históricos de malária.")