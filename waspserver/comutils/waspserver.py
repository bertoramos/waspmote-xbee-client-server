
from digi.xbee.devices import ( XBeeDevice,
                                RemoteXBeeDevice,
                                XBeeException )

import time
import logging

import threading

from . import commands

class WaspServer:

    def __init__(self, usb="/dev/ttyUSB0", freq=115200):
        self._device = XBeeDevice(usb, freq)
        try:
            self._device.open()
        except XBeeException:
            logging.error("Error while opening xbee")

        self._reachable_devices = {}

    def close_server(self):
        self._device.close()
        try:
            logger = logging.getLogger("waspserver")
            logger.info(" *** Server closed")
            print(" *** Server closed")
        except:
            pass
    
    def start_scanner(self, scan_time=10, deeptime=10):

        def scan():
            while self._device.is_open():
                print(" *** Start scanning *** ")

                # Scan network
                xnet = self._device.get_network()

                xnet.start_discovery_process(deep=True, n_deep_scans=1)

                while xnet.is_discovery_running():
                    time.sleep(0.5)

                nodes = xnet.get_devices()
                new_remotes = {}

                infostr = " *** All reachable devices ***\n"
                for n in nodes:
                    new_remotes[str(n.get_64bit_addr())] = n
                    infostr += "\t" + str(n)

                logger = logging.getLogger("waspserver")
                logger.info(infostr)
                print(infostr)

                avail_remotes = {}
                # Communicate with new remotes
                for k in new_remotes.keys():
                    new_dev = new_remotes[k]

                    if commands.generate_start_communication(self._device, new_dev, deeptime):
                        logger = logging.getLogger("waspserver")
                        logger.info(f"{k} connected!\n")

                self._reachable_devices = new_remotes

                time.sleep(scan_time)

        thread = threading.Thread(target=scan, daemon=True)
        thread.start()

    def recv_message(self):

        def recv_fun():
            logger = logging.getLogger("waspserver")
            while True:
                try:
                    # Receive message from any source
                    msg = self._device.read_data()

                    if msg is not None: # Receive message ?

                        # Ignore previously undetected devices
                        addr = str(msg.remote_device.get_64bit_addr())
                        if addr not in self._reachable_devices.keys():
                            continue

                        # Checks if message is a status packet
                        if commands.parse_status_packet(msg):
                            logger.info(f"Parse status packet received : {msg.data.decode()} from {msg.remote_device.get_64bit_addr()}")
                            continue

                except Exception as ex:
                    logger.debug(f"{ex}")

        thread = threading.Thread(target=recv_fun, daemon=True)
        thread.start()

    def loop(self):
        try:
            while True:
                self.__loop()
        except KeyboardInterrupt:
            self.close_server()

    def __loop(self):
        pass

    def __del__(self):
        self.close_server()
