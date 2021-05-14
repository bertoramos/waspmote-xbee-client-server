
import time
from datetime import datetime
import logging

def generate_start_communication(device, remote, deeptime):
    """
    Sends a start_communication message to waspmote

        Format : TYPE|UNIXTIME|SLEEPTIME
            TYPE : message identifier
            UNIXTIME : unix timestamp
            SLEEPTIME : deep sleep time in seconds

    Params:
        + device : pc xbee
        + remote : remote device

    Returns:
        + bool : True if message was sent correctly
    """
    logger = logging.getLogger("waspserver")

    try:
        now_date = datetime.now()
        yy = now_date.year % 100
        mm = now_date.month
        dd = now_date.day
        wd = now_date.weekday()
        HH = now_date.hour
        MM = now_date.minute
        SS = now_date.second

        #strdate = f"{yy}:{mm:02d}:{dd:02d}:{wd:02d}:{HH:02d}:{MM:02d}:{SS:02d}"
        d = datetime.now()
        unixtime = time.mktime(d.timetuple())
        msgdata = "0|" + str(int(unixtime)) + "|" + str(deeptime)
        device.send_data(remote, msgdata)

        logger.info(msgdata)
    except Exception as ex:
        logger.debug(f"{ex}")
        return False

    try:

        for e in range(10):
            data = device.read_data_from(remote)
            if data is not None:
                break
            time.sleep(1)

        if data is not None:
            print(data.data.decode())
            return True

        return False
    except:
        return False

    return True

###########

def parse_status_packet(msg):
    """
    Parse a status message

        Format : TYPE|UNIXTIME|XANG|YANG|ZANG|BATT|INTC
            TYPE : message identifier
            UNIXTIME : unix timestamp
            XANG : x-axis angle
            YANG : y-axis angle
            ZANG : z-axis angle
            BATT : battery percentage
            INTC  : interruption cause ( 0 : Unknown | 1 : Accelerometer | 2 : Timeout )

    Params:
        + msg : message received
    Returns:
        + bool : True if msg is a status message
    """
    data = msg.data.decode()
    src = msg.remote_device.get_64bit_addr()

    cmd = data.split("|")

    packet_type = int(cmd[0])
    if packet_type == 1:
        unix_time = int(cmd[1])
        xacc = int(cmd[2])
        yacc = int(cmd[3])
        zacc = int(cmd[4])
        batt = float(cmd[5])
        intc = int(cmd[6])

        causes = { 0: "Unknown",
                   1: "Waspmote was moved",
                   2: "Timeout" }

        print(f"\n\n *** Waspmote {src} status *** ")
        print("\t", datetime.fromtimestamp(unix_time).strftime("%a, %Y/%m/%d, %H:%M:%S"))
        print(f"\t(x,y,z) = ({xacc}, {yacc}, {zacc})")
        print(f"\tBattery level = {batt} %")
        print(f"\tInterruption cause : {causes[intc]}\n\n")
        return True

    return False
