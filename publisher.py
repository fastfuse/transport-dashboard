import logging
from time import sleep

from sqlalchemy.exc import OperationalError

from application import models, tasks

log = logging.getLogger('Publisher')

if __name__ == '__main__':

    while True:
        try:
            log.info('Start...')

            stops = models.Stop.query.all()

            log.info(f"Found {len(stops)} stops")

            stops_codes = [stop.code for stop in stops]

            for code in stops_codes:
                log.info(f"Getting info for stop code {code}")
                tasks.get_stop_info.delay(code)

            log.info('Sleep...')
            sleep(30)

        except OperationalError as e:
            log.warning('Could not connect to PSQL. Sleep...')
            sleep(5)

# TODO: switch to celery beat
