# Funções auxiliares para o projeto SentinelaMSF
import logging
import os
from dotenv import load_dotenv

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sentinela.log', mode='a')
        ]
    )
    logging.info('Logging configurado.')
    load_dotenv()
