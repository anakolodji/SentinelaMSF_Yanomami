import pandas as pd
from datetime import datetime
from sentinela.db import MalariaCaso, SessionLocal, Base, engine

def ingest_malaria_cases(csv_path):
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        caso = MalariaCaso(
            municipio=row['municipio'],
            data=datetime.strptime(row['data'], '%Y-%m-%d'),
            casos=int(row['casos'])
        )
        db.add(caso)
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    # Exemplo de uso: ingest_malaria_cases('malaria_historico.csv')
