import pandas as pd
from sentinela.db import EnchenteDetectada, SessionLocal, Base, engine
import sys
from datetime import datetime

def ingest_enchentes(csv_path):
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        registro = EnchenteDetectada(
            municipio=row.get('municipio') or row.get('Município'),
            data=pd.to_datetime(row['data']),
            area_alagada_km2=float(row.get('area_alagada_km2', 0)),
            imagem_path=row.get('imagem_path'),
            # Caso existam colunas latitude/longitude
            # latitude=float(row.get('latitude', 0)),
            # longitude=float(row.get('longitude', 0))
        )
        db.add(registro)
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    if len(sys.argv) < 2:
        print('Uso: python ingest_enchentes.py caminho/para/arquivo.csv')
    else:
        ingest_enchentes(sys.argv[1])
