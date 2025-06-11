import pandas as pd
from sentinela.db import AlertaINMET, SessionLocal, Base, engine
import sys
from datetime import datetime

def ingest_alertas(csv_path):
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        registro = AlertaINMET(
            regiao=row.get('municipio') or row.get('Município') or row.get('regiao'),
            data_emissao=pd.to_datetime(row.get('data') or row.get('data_emissao')),
            tipo=row.get('tipo'),
            descricao=row.get('descricao'),
            fonte=row.get('fonte', 'INMET')
        )
        db.add(registro)
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    if len(sys.argv) < 2:
        print('Uso: python ingest_alertas.py caminho/para/arquivo.csv')
    else:
        ingest_alertas(sys.argv[1])
