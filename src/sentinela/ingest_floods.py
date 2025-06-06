import pandas as pd
from datetime import datetime
from sentinela.db import EnchenteDetectada, SessionLocal, Base, engine

def ingest_floods(csv_path):
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        flood = EnchenteDetectada(
            municipio=row['municipio'],
            data=datetime.strptime(row['data'], '%Y-%m-%d'),
            area_alagada_km2=float(row['area_alagada_km2']),
            imagem_path=row.get('imagem_path', None)
        )
        db.add(flood)
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    # Exemplo de uso: ingest_floods('floods_detected.csv')
