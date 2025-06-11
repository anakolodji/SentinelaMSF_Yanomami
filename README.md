# Sentinela MSF - Yanomami

## Visão Geral

Esta plataforma foi desenvolvida para apoiar o MSF (Médicos Sem Fronteiras) na alocação eficiente de recursos e monitoramento de surtos de malária em regiões vulneráveis a enchentes, integrando dados ambientais, epidemiológicos, geoespaciais e climáticos.

- **Notebook principal:** `notebooks/SentinelaMSF_MSF_final.ipynb`
- **Painel interativo:** Streamlit (`src/sentinela/services/app.py`)
- **Integração climática:** Weather API (chave no arquivo `.env`)

## Funcionalidades
- Ingestão e processamento de dados ambientais, malária, enchentes e alertas.
- Engenharia de atributos e modelagem preditiva de risco.
- Visualização geoespacial dos riscos e alertas em tempo real.
- Consulta de condições climáticas atuais por município.

## Como executar o painel Streamlit

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure sua chave da Weather API no arquivo `.env` na raiz do projeto:
   ```env
   WEATHER_API_KEY=suachaveaqui
   ```
3. Execute o painel:
   ```bash
   streamlit run src/sentinela/services/app.py
   ```
4. Acesse o painel pelo navegador no endereço exibido (ex: http://localhost:8501)

## Como utilizar o notebook
Abra o arquivo `notebooks/SentinelaMSF_MSF_final.ipynb` em seu ambiente Jupyter ou Colab para explorar todas as etapas do pipeline, desde a ingestão até a visualização dos resultados.

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

---

## Fluxo de Dados e Ingestão

1. **Ingestão Automática de Alertas Climáticos**
   - O script `src/scheduler.py` agenda a ingestão de alertas a cada 6h usando APScheduler.
   - Os dados são obtidos da WeatherAPI e salvos no banco SQLite.
   - Logs são salvos em `sentinela.log`.

2. **Ingestão Manual de Casos de Malária e Predições**
   - Use os scripts `src/sentinela/ingest_malaria.py` e `src/sentinela/ingest_predicoes.py` para importar dados históricos via CSV.
   - O sistema evita duplicidade automaticamente.

3. **Interface Streamlit**
   - Execute `src/app.py` para abrir o dashboard interativo.
   - A interface lê apenas do banco local, não consulta APIs externas diretamente.
   - Filtros, mapas, estatísticas e alertas são exibidos de forma acessível.

---

## Uso do Scheduler

Para iniciar o agendamento automático de ingestão climática:
```bash
python src/scheduler.py
```
O script rodará em background e fará a coleta a cada 6h.

---

## Testes Unitários

Os testes de ingestão estão em `tests/test_ingest.py`.
Execute:
```bash
pytest tests/test_ingest.py
```
Isso garante que duplicidades são evitadas e a ingestão funciona corretamente.

---

## Dicas para Usuários
- Configure variáveis de ambiente no arquivo `.env` (ex: chaves de API).
- Consulte os logs em `sentinela.log` para depuração.
- Para atualizar alertas manualmente, use o botão na interface Streamlit.
- Ajuste coordenadas reais no mapa conforme necessário.

---

## Contato
Dúvidas ou sugestões? Abra uma issue ou entre em contato com a equipe do projeto.
