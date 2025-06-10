"""
Scheduler para ingestão automática de alertas climáticos a cada 6h.
"""
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from sentinela.ingest_weather import ingest_weather_alerts
import logging
from sentinela.utils import setup_logging

def main():
    setup_logging()
    scheduler = BlockingScheduler()
    scheduler.add_job(ingest_weather_alerts, 'interval', hours=6, id='weather_alerts_job')
    logging.info('Scheduler iniciado: ingestão de alertas climáticos a cada 6h.')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info('Scheduler finalizado.')

if __name__ == "__main__":
    main()
