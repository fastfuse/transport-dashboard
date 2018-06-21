from time import sleep

from app import models
from app.tasks import get_stop_info
from app.utils import *

t = TransportAPIWrapper()


if __name__ == '__main__':

    stops = models.Stop.query.all()
    stops_codes = [stop.code for stop in stops]

    while True:
        print('Start...')

        stops = models.Stop.query.all()

        stops_codes = [stop.code for stop in stops]

        routes = t.get_all_routes()

        for code in stops_codes:
            get_stop_info.delay(code)

        print('sleep...')
        sleep(30)

# TODO:
# * handle errors;
# * add logging;


# * requests timeout + retry investigate

# pseudocode:
# while true:
#     ...
#     for stop in stops:
#         execute(stop)
#
#     sleep(30)

# looks_lively_listener
