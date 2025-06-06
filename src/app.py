import streamlit as st
st.set_page_config(page_title="SentinelaMSF Yanomami", layout="wide")
import pandas as pd
from sentinela.db import SessionLocal, AlertaINMET, MalariaCaso, EnchenteDetectada, PredicaoRisco
import folium
from streamlit_folium import st_folium

st.title("SentinelaMSF Yanomami: Monitoramento de Riscos")

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
risco_filter = st.sidebar.selectbox("Nível de Risco", ["Todos", "alto", "medio", "baixo"])

# Botão para atualizar alertas
if st.sidebar.button("Atualizar Alertas Climáticos"):
    from sentinela.ingest_weather import ingest_weather_alerts
    ingest_weather_alerts()
    st.sidebar.success("Alertas atualizados!")

# Exibir alertas recentes
st.subheader("Últimos Alertas Climáticos")
alertas = get_alertas()
if alertas:
    for alerta in alertas[:5]:
        st.warning(f"[{alerta.data_emissao.strftime('%d/%m/%Y %H:%M')}] {alerta.tipo} - {alerta.regiao}\n{alerta.descricao}")
else:
    st.info("Nenhum alerta recente disponível.")

# Exibir estatísticas rápidas
st.subheader("Estatísticas de Risco")
predicoes = get_predicoes()
if predicoes:
    df_pred = pd.DataFrame([{ 'Município': p.municipio, 'Risco': p.risco, 'Score': p.score } for p in predicoes])
    if risco_filter != "Todos":
        df_pred = df_pred[df_pred['Risco'] == risco_filter]
    top5 = df_pred.sort_values('Score', ascending=False).head(5)
    st.table(top5)
else:
    st.info("Sem predições de risco disponíveis.")

# Mapa interativo
st.subheader("Mapa de Risco e Enchentes")
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
        folium.Marker(
            location=[-0.5, -64.5],  # Ajustar para coordenadas reais se disponíveis
            popup=f"{p.municipio}: Risco ALTO ({p.score:.2f})",
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(mapa)

st_folium(mapa, width=900, height=500)

# Evolução dos casos de malária
st.subheader("Evolução dos Casos de Malária")
casos = get_malaria_casos()
if casos:
    df_casos = pd.DataFrame([{ 'Município': c.municipio, 'Data': c.data, 'Casos': c.casos } for c in casos])
    st.line_chart(df_casos.groupby('Data')['Casos'].sum())
else:
    st.info("Sem dados históricos de malária.")

# (Opcional) Mapa e visualização espacial podem ser adicionados com folium/streamlit-folium