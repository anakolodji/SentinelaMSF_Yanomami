import pandas as pd
from datetime import datetime
from sentinela.db import MalariaCaso, SessionLocal, Base, engine
import logging
from sentinela.utils import setup_logging

def ingest_malaria_cases(csv_path):
    setup_logging()
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    inseridos = 0
    ignorados = 0
    for _, row in df.iterrows():
        municipio = row['municipio']
        data = datetime.strptime(row['data'], '%Y-%m-%d')
        casos = int(row['casos'])
        exists = db.query(MalariaCaso).filter_by(municipio=municipio, data=data).first()
        if exists:
            logging.info(f'Caso duplicado ignorado: {municipio} - {data.date()}')
            ignorados += 1
            continue
        caso = MalariaCaso(
            municipio=municipio,
            data=data,
            casos=casos
        )
        db.add(caso)
        inseridos += 1
    db.commit()
    db.close()
    logging.info(f'Casos inseridos: {inseridos}, duplicados ignorados: {ignorados}')

if __name__ == "__main__":
    setup_logging()
    Base.metadata.create_all(bind=engine)
    # Exemplo de uso: ingest_malaria_cases('malaria_historico.csv')
