import os
import sys
import threading
import time

from config import config
from app.smartmeter import smartmeter

smartmeters = {}

def _run_smart_meter_for_uid(uid):
    smart_meter = smartmeter.SmartMeter(uid)
    smart_meter.run_smart_meter(60, 1)

def start_smart_meters_in_parallel(path):
    for subdir, _, _ in os.walk(path):
        if subdir.startswith(path + "/"):
            uid = subdir.split("/")[-1]
            thread = threading.Thread(target=_run_smart_meter_for_uid, args=(uid,))
            print("Smartmeter mit der UID: " + uid + " gestartet", file=sys.stderr)
            smartmeters[uid] = thread
            thread.do_run = True
            thread.start()

def check_for_changed_smart_meters(path):
    global smartmeters
    current_uids = set(subdir.split("/")[-1] for subdir, _, _ in os.walk(path) if subdir.startswith(path + "/"))
    existing_uids = set(smartmeters.keys())

    # Check for new smart meters
    new_uids = current_uids - existing_uids
    for uid in new_uids:
        thread = threading.Thread(target=_run_smart_meter_for_uid, args=(uid,))
        print("Neuer Smartmeter mit der UID: " + uid + " gestartet", file=sys.stderr)
        smartmeters[uid] = thread
        thread.start()

    # Check for deleted smart meters
    deleted_uids = existing_uids - current_uids
    for uid in deleted_uids:
        thread = smartmeters.pop(uid)
        thread.do_run = False
        thread.join()  # Wait for the thread to finish

        print("Smartmeter mit der UID: " + uid + " beendet", file=sys.stderr)

if __name__ == '__main__':
    start_smart_meters_in_parallel(config.CertificateConfig.CERT_DIRECTORY)

    while True:
        time.sleep(5)
        check_for_changed_smart_meters(config.CertificateConfig.CERT_DIRECTORY)