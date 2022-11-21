from json import load
from tabulate import tabulate
from datetime import datetime, timedelta
import time


class Parse:

    def print_android_accelerometer(self, accel):
        print("Printing accelerometer records.")

        records = accel["records"]
        record_time = self.pp_kw_epoch(records[0]["timestamp"])
        print(tabulate(records, headers="keys"))

        print("Printing accelerometer metadata.")
        # We could just iterate through these, but doing it explicitly in
        # order to provide a more helpful example.
        table = list()
        table.append(["first record time", record_time])
        table.append(["type",       accel["type"]])
        table.append(['platform',   accel['platform']])
        table.append(['clientId',   accel['clientId']])
        table.append(['dataSize',   accel['dataSize']])
        table.append(['numRecords', accel['numRecords']])
        table.append(['startTime',  self.pp_kw_epoch(accel['startTime'])])
        table.append(['endTime',    self.pp_kw_epoch(accel['startTime'])])

        print(tabulate(table, headers=["Field", "Value"]))

    # JSON parsing is very simple, just providing here for conveninence:
    def parse_android_accelerometer(self, theFile):
        return load(theFile)

    # Pretty-print KW's version of epoch without ms
    def pp_kw_epoch(self, stamp):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp/1000))
