import pandas as pd
from sentinela.db import VulnerabilidadeInundacao, SessionLocal, Base, engine
import sys

# Exemplo de uso: python ingest_vulnerabilidade.py caminho/para/arquivo.csv

def ingest_vulnerabilidade(csv_path):
    df = pd.read_csv(csv_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        registro = VulnerabilidadeInundacao(
            municipio=row.get('municipio') or row.get('Município'),
            ano=int(row['data'] if 'data' in row else row['ano']),
            indice_vulnerabilidade=float(row.get('indice_vulnerabilidade', 0)),
            area_indigena=float(row.get('Área Indígena', 0)),
            area_urbana=float(row.get('Área Urbana', 0)),
            area_rural=float(row.get('Área Rural', 0)),
            area_garimpo=float(row.get('Área de Garimpo', 0)),
            area_assentamento=float(row.get('Área de Assentamento', 0)),
            total_geral=float(row.get('Total Geral', 0))
        )
        db.add(registro)
    db.commit()
    db.close()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    if len(sys.argv) < 2:
        print('Uso: python ingest_vulnerabilidade.py caminho/para/arquivo.csv')
    else:
        ingest_vulnerabilidade(sys.argv[1])
