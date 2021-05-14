
from digi.xbee.util import utils

from comutils import WaspServer
import logging
import datetime
from pathlib import Path

import parseinput

def init_log():
    path = Path("./logs/")
    path.mkdir(exist_ok=True, parents=True)

    logfile = path / Path(datetime.datetime.now().strftime("log_%m%d%Y_%H%M%S") +".log")

    logger = logging.getLogger("waspserver")
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", '%Y-%m-%d %H:%M:%S')

    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


if __name__ == '__main__':
    scantime, notify_time, usb = parseinput.parse()

    print("Program starts")

    init_log()

    server = WaspServer(usb=usb)
    server.start_scanner(scan_time=scantime, deeptime=notify_time)
    server.recv_message()

    server.loop()
