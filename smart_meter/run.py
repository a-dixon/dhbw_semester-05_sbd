import os
import sys
import threading
import time

from config import config
from app.smartmeter import smartmeter

smartmeters = []


def _run_smart_meter_for_uid(uid):
    smart_meter = smartmeter.SmartMeter(uid)
    smart_meter.run_smart_meter(60, 1)


def start_smart_meters_in_parallel(path):
    for subdir, _, _ in os.walk(path):
        if subdir.startswith(path + "/"):
            uid = subdir.split("/")[-1]
            thread = threading.Thread(target=_run_smart_meter_for_uid, args=(uid,))
            print("Smartmeter mit der UID: " + uid + " gestartet", file=sys.stderr)
            smartmeters.append(uid)
            thread.start()


def check_for_new_smart_meters(path):
    for subdir, _, _ in os.walk(path):
        if subdir.startswith(path + "/"):
            uid = subdir.split("/")[-1]
            if uid not in smartmeters:
                thread = threading.Thread(target=_run_smart_meter_for_uid, args=(uid,))
                print("Smartmeter mit der UID: " + uid + " gestartet", file=sys.stderr)
                smartmeters.append(uid)
                thread.start()


if __name__ == '__main__':
    start_smart_meters_in_parallel(config.CERT_DIRECTORY)

    while True:
        time.sleep(5)
        check_for_new_smart_meters(config.CERT_DIRECTORY)
