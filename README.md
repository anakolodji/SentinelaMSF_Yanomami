# Sentinela MSF - Yanomami

## Estrutura do Projeto

```
SentinelaMSF_Yanomami/
│
├── src/
│   └── sentinela/
│       ├── __init__.py
│       ├── utils.py
│       ├── database.py
│       ├── models/
│       │   └── __init__.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── app.py
│       ├── processing/
│       │   ├── __init__.py
│       │   └── load_shapefiles.py
│       └── data/
│           └── __init__.py
│
├── data/
│   ├── raw/           # Dados brutos
│   └── processed/     # Dados processados
│
├── notebooks/         # Notebooks Jupyter para análises
│
├── requirements.txt   # Dependências do projeto
│
└── README.md
```

## Organização
- **models/**: Classes de entidades do domínio (ex: Usuário, DadoGeográfico, etc).
- **services/**: Lógica de negócio e serviços (ex: processamento de dados, validações, app principal).
- **processing/**: Scripts e funções para ingestão e processamento de dados.
- **utils.py**: Funções auxiliares.
- **data/raw/**: Dados brutos.
- **data/processed/**: Dados já tratados/processados.
- **notebooks/**: Notebooks Jupyter para exploração e análise.
- **requirements.txt**: Lista única de dependências do projeto.

## Dicas
- Sempre inclua um `__init__.py` nas pastas de código.
- Para APIs, considere usar FastAPI ou Flask.
- Para banco de dados, considere usar SQLAlchemy.
- Mantenha a documentação e dependências sempre atualizadas.
