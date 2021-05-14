
import argparse
import sys

def parse():
    parser = argparse.ArgumentParser(description="Waspserver")
    parser.add_argument("--scantime", required=False, default=10, choices=range(5,60), help="Frequency at which the server scan network", type=int, metavar="[5-60]")
    parser.add_argument("--notify_time", required=False, type=int, default=10, choices=range(5,60), metavar="[5-60]", help="Frequency at which the client notify state")
    parser.add_argument("--usb", required=False, type=str, default="/dev/ttyUSB0", help="Xbee device (default : /dev/ttyUSB0)")
    args = parser.parse_args()
    scantime = args.scantime
    notify_time = args.notify_time
    usb = args.usb

    if not 5 <= scantime <= 59:
        parser.error("error in scantime range")
        parser.print_help(sys.stderr)
        sys.exit(1)

    if not 5 <= notify_time <= 59:
        parser.error("error in notify_time range")
        parser.print_help(sys.stderr)
        sys.exit(1)

    return scantime, notify_time, usb
