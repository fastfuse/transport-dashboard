import json
import logging
from collections import namedtuple
from time import sleep

from sqlalchemy.exc import OperationalError

from application import models, tasks, utils

t = utils.TransportAPIWrapper()

log = logging.getLogger('Publisher')

if __name__ == '__main__':

    while True:
        try:
            stops = models.Stop.query.all()
            stops_codes = [stop.code for stop in stops]

            log.info('Start...')

            stops = models.Stop.query.all()
            stops_codes = [stop.code for stop in stops]

            for code in stops_codes:
                tasks.get_stop_info.delay(code)

            log.info('Sleep...')
            sleep(30)

        except OperationalError as e:
            log.warning('Could not connect to PSQL. Sleep...')
            sleep(5)

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

# use flask's log?


import lxml.html
import requests
from collections import namedtuple

data = requests.get("https://lad.lviv.ua/stops")

stop = namedtuple("Stop", ['name', 'longitude', 'latitude', 'external_id', 'code'])

parsed_stops_root = lxml.html.fromstring(data.text)

stops_data = [[child.text for child in ps.getchildren()] for ps in parsed_stops_root.xpath('//tr')[1:]]

stops_objects = [stop(*s[:-1]) for s in stops_data]

stops = {stop.code: stop._asdict() for stop in stops_objects}

json.dumps(stops)
