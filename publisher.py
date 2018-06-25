import logging
from time import sleep

from application import models, tasks, utils

t = utils.TransportAPIWrapper()

log = logging.getLogger('Publisher')

if __name__ == '__main__':

    stops = models.Stop.query.all()
    stops_codes = [stop.code for stop in stops]

    while True:
        log.info('Start...')

        stops = models.Stop.query.all()
        stops_codes = [stop.code for stop in stops]

        for code in stops_codes:
            tasks.get_stop_info.delay(code)

        log.info('Sleep...')
        sleep(30)

# TODO:
# * fix imports issue
# * handle errors;

# * requests timeout + retry investigate

# pseudocode:
# while true:
#     ...
#     for stop in stops:
#         execute(stop)
#
#     sleep(30)

# looks_lively_listener
