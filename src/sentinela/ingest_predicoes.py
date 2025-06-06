import pandas as pd
from datetime import datetime
from sentinela.db import PredicaoRisco, SessionLocal, Base, engine

def ingest_predicoes(csv_path):
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        pred = PredicaoRisco(
            municipio=row['municipio'],
            data=datetime.strptime(row['data'], '%Y-%m-%d'),
            risco=row['risco'],
            score=float(row['score'])
        )
        db.add(pred)
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    # Exemplo de uso: ingest_predicoes('predicoes.csv')
