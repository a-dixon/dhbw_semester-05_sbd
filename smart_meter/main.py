import os
import threading
from smart_meter.smartmeter import smartmeter

smart_meters = []


def _run_smart_meter_for_uid(uid):
    smart_meter = smartmeter.SmartMeter(uid)
    smart_meter.run_smart_meter()
    smart_meters.append(smart_meter)


def start_smart_meters_in_parallel(path):
    for subdir, _, _ in os.walk(path):
        if subdir.startswith(path + "/"):
            uid = subdir.split("/")[-1]
            thread = threading.Thread(target=_run_smart_meter_for_uid, args=(uid,))
            print("Smartmeter mit der UID: " + uid + " gestartet")
            thread.start()
