import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from sentinela.db import AlertaINMET, SessionLocal, Base, engine

load_dotenv()

# Configurações
API_KEY = os.getenv('WEATHER_API_KEY')
# Exemplo: região Yanomami (RR)
REGIONS = [
    {"name": "Yanomami", "lat": -0.5, "lon": -64.5},
    # Adicione outras regiões se necessário
]

# Exemplo de endpoint WeatherAPI para alertas climáticos
BASE_URL = "http://api.weatherapi.com/v1/alerts.json"

def fetch_weather_alerts(region):
    params = {
        "key": API_KEY,
        "q": f"{region['lat']},{region['lon']}"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar alertas: {response.status_code}")
        return None

def save_alerts_to_db(alerts, region_name, db: Session):
    # Adicionar log para depuração
    print('DEBUG: Conteúdo dos alerts retornados:', alerts)
    # A estrutura correta da WeatherAPI pode variar, normalmente é alerts['alerts']['alert']
    alert_list = []
    if 'alerts' in alerts and 'alert' in alerts['alerts']:
        alert_list = alerts['alerts']['alert']
    if not alert_list:
        print(f"Nenhum alerta encontrado para {region_name}.")
        return
    for alert in alert_list:
        # A WeatherAPI pode não ter o campo 'date', normalmente é 'effective' ou 'expires'
        data_emissao_str = alert.get('effective') or alert.get('expires') or alert.get('date')
        if data_emissao_str:
            try:
                data_emissao = datetime.strptime(data_emissao_str[:16], '%Y-%m-%dT%H:%M')
            except Exception:
                data_emissao = datetime.now()
        else:
            data_emissao = datetime.now()
        db_alert = AlertaINMET(
            regiao=region_name,
            data_emissao=data_emissao,
            tipo=alert.get('event', 'N/A'),
            descricao=alert.get('headline', '') + "\n" + alert.get('desc', ''),
            fonte=alert.get('source', 'WeatherAPI')
        )
        db.add(db_alert)
    db.commit()


def ingest_weather_alerts():
    db = SessionLocal()
    for region in REGIONS:
        alerts = fetch_weather_alerts(region)
        if alerts:
            save_alerts_to_db(alerts, region['name'], db)
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    ingest_weather_alerts()
    print("Ingestão de alertas climáticos concluída.")
