from json import load
import e3db
from e3db.types import Search
from tabulate import tabulate
import os
import sys
from datetime import datetime, timedelta
import time
from wash.types import Types
from wash.parse import Parse


class Commands:
    downloads_path = "./downloads"
    example_survey_record_id = "47f4c1bd-f308-4c7a-ac80-bd0622fcf767"
    example_accel_record_id = "d2ebdf48-af0e-41cf-8b3e-b2dbc3aa5150"

    def __init__(self, c):
        self.client = c
        self.total_downloaded = 0

# ------------------------ Your Test Here ---------------------------
    def user_test(self):
        print("User test here.")

# --------------------------- Commands -------------------------------

    def smoke_test(self, namespace):
        print("Able to link into the WASH library.")
        print("Config file location: " + Commands.config_location())

        print("Querying a record we know should exist.")
        step_counter = "bd2a7c0b-21c0-48db-b9c4-b088cf9a8cbe"
        FileMeta = self.client.read_file(step_counter, "sensor-output.txt")
        print("Done fetching. Reading file.")

        with open("sensor-output.txt", "r") as f:
            json_version = load(f)
        print("JSON version: " + str(json_version))
        expected_startTime = 1589803124621
        if (json_version["startTime"] == expected_startTime):
            print("Start time is correct at: " + str(expected_startTime))
        else:
            print("Something went wrong because got startTime : "
                  + str(json_version["startTime"]) + " instead of " + str(expected_startTime))
            return False

        return True

    def print_record(self, namespace):
        print("Printing a record: " + namespace.record_id)
        record = self.client.read(namespace.record_id)
        print("Record ID:\t" + str(record.meta.record_id))
        print("User ID:\t" + str(record.meta.user_id))
        print("Writer ID:\t" + str(record.meta.writer_id))
        print("Queryable Metadata:")
        for key in record.meta.plain:
            print("\t" + key + "\t" + record.meta.plain[key])

        print("Decrypted Data (besides the file, if any):")
        for key in record.data:
            print("\t" + key + "\t" + record.data[key])

        if not namespace.nodownload:
            # TODO Only download the file if there is file data:
            print("The Download File (output.txt):")
            FileMeta = self.client.read_file(
                record.meta.record_id, "output.txt")
            with open("output.txt", "r") as f:
                json_version = load(f)
                print(str(json_version))

    def sensor_count(self, namespace):
        print("Printing one copy of each sensor since Feb 1 until now:")
        self.check_all_sensors(Commands.fromisoformat(
            "2020-02-01"), datetime.now())
        return True

    def query_records(self, namespace):
        if (namespace.start_date == None):
            start_str = "2020-05-01"
        else:
            start_str = namespace.start_date

        if (namespace.end_date == None):
            end_str = "2020-05-31"
        else:
            end_str = namespace.end_date

        # Time and date range computation
        start = Commands.fromisoformat(start_str)
        end = Commands.fromisoformat(end_str)
        rec_types = []
        if namespace.rectype:
            rec_types = [namespace.rectype]
        if namespace.recfile:
            rec_types = [r.strip()
                         for r in open(namespace.recfile).readlines()]

        self.print_records_type(namespace.number, rec_types,
                                namespace.download, start, end, page=namespace.page)

    def list_sensors(self, namespace):
        for sensor in sorted(Types.all_sensors()):
            print(sensor)

    def example_android_accel_parse(self, namespace):
        query = Search(count=1, include_data=True,
                       include_all_writers=True, next_token=0).match(record_types=["a-kry-sensor-accelerometer"])
        results = self.client.search(query)
        if len(results) == 0:
            print("Records not found.  Ensure your client has been approved for access")
            return
        for record in results:  # just do this once actually
            self.client.read_file(
                record.meta.record_id, "output.txt")
            with open("output.txt", "r") as f:
                parse = Parse()
                data = parse.parse_android_accelerometer(f)
                parse.print_android_accelerometer(data)
            return  # exits after the first time through loop

    def example_altitude_weekly(self, namespace):
        table = list()
        start_str = "2020-02-01"
        start = Commands.fromisoformat(start_str)
        end = start + timedelta(days=6)
        running_total = 0
        while (start < (datetime.now() + timedelta(days=1))):  # end at tomorrow
            query = Search(include_data=False,
                           include_all_writers=True, next_token=0).match(condition="AND", record_types=["i-kry-sensor-altitude"]).range(start=start, end=end)
            results = self.client.search(query)
            running_total += results.total_results
            row = [str(start), str(end), str(
                results.total_results), running_total]
            table.append(row)
            start = end + timedelta(days=1)
            end = start + timedelta(days=6)

        print(tabulate(table, headers=[
              "Start", "End", "Record Count", "Running Total"]))

    def example_check_fever(self, namespace):
        quit_after_records = 200  # just to prevent lots of unnecessary data...
        query_items = {}

        # Create a query data structure for every day of the week
        # where users report "Yes". These uuids are hard-coded in the
        # types file. See the spreadsheet for complete data.
        # Also demonstrates iterating through the list.

        for survey_uuid in Types.example_fever_every_day:
            query_items[survey_uuid] = "Yes"

        query = Search(count=10, include_data=True,
                       include_all_writers=True, next_token=0).match(plain=query_items)
        results = self.client.search(query)
        if len(results) == 0:
            print("Records not found.  Ensure your client has been approved for access")
            return
        print("Total results: " + str(results.total_results))
        i = 0  # counter for enumerating

        while results.next_token:  # Page through results:
            results = self.client.search(query)

            for record in results:
                # Now do something with each type e.g. fetch more data for that user:
                print(str(i) + "\t Writer ID: " + str(record.meta.writer_id))
                i = i + 1

            query.next_token = results.next_token
            if i >= quit_after_records:  # Exit to prevent lots of unnecessary data
                break

# --------------------------- Helpers -------------------------------
    @staticmethod
    def fromisoformat(date_str):
        """
        Converts a date string in the iso format (i.e 2020-05-01 01:03:04) to
        a datetime object.

        :param date_str - string
            a string containing the date to convert in the iso format
        :return datetime object
        """
        try:
            return datetime.fromisoformat(date_str)  # python3.7
        except AttributeError:  # python3.7 and less compatible
            if ":" in date_str:
                return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            else:
                return datetime.strptime(date_str, '%Y-%m-%d')

    @staticmethod
    def config_location():
        config_name = "wash-fedramp"
        home = os.path.expanduser('~')
        check_dir = "./credentials.json"
        check_home = os.path.join(home, '.tozny', config_name, 'e3db.json')

        if os.path.exists(check_dir):
            return check_dir
        elif os.path.exists(check_home):
            return check_home
        else:
            sys.exit("Can't find config file in " +
                     check_dir + " or " + check_home + ".")

    @staticmethod
    def load_client():
        return e3db.Client(load(open(Commands.config_location())))

    def print_records(self, results):
        # Collect all records in a list
        table = list()
        if len(results) == 0:
            print("Records not found.  Ensure your client has been approved for access")

        for record in results:
            # Combine sensitive info with plaintext meta
            also_print = {"record_id": record.meta.record_id}
            row = dict(record.data)
            row.update(record.meta.plain)
            row.update(also_print)
            table.append(row)

            # Print a table of records. (Using tabulate, from https://pypi.org/project/tabulate/)
        print(tabulate(table, headers="keys"))

    def download_records(self, results):
        if len(results) == 0:
            print("Records not found.  Ensure your client has been approved for access")

        for record in results:
            record_id = record.meta.record_id
            user_id = record.meta.user_id
            device_id = record.meta.plain.get('device_id', -1)
            if device_id == -1:
                device_id = record.meta.plain.get('android_id', "NA")
            first_ts = record.meta.plain.get('first_timestamp', "")
            last_ts = record.meta.plain.get('last_timestamp', "")
            orig_fn = record.meta.plain.get("original_file_name", "")

            write_path = os.path.join(
                self.downloads_path, str(user_id),  str(device_id))

            os.makedirs(write_path, exist_ok=True)

            dest = os.path.join(write_path, '_'.join(
                [first_ts, last_ts, orig_fn]))
            FileMeta = self.client.read_file(record.meta.record_id, dest)

    def print_records_type(self, number, rectype, do_download, start, end, next_token=0, page=True):
        if (rectype == None): exit ("Cannot query on None records type.")
        print("Querying " + str(number) + " records of type: " +
              str(rectype) + " from " + str(start) + " to " + str(end))
        if isinstance(rectype, str):
            rectype = [rectype]
        query = Search(count=number, include_data=True,
                       include_all_writers=True, next_token=next_token).match(condition="OR", record_types=rectype).range(start=start, end=end)

        results = self.client.search(query)
        new_next = results.next_token
        print("Total results: " + str(results.total_results))
        self.print_records(results)
        if (do_download):
            print("Downloading files into ./downloads")
            self.download_records(results)
        self.total_downloaded += int(number)
        if page:
            if self.total_downloaded <= results.total_results:
                self.print_records_type(
                    number, rectype, do_download, start, end, new_next, page)

    def check_all_sensors(self, start, end):
        table = list()
        total = 0
        for sensor_type in Types.all_sensors():
            query = Search(count=1, include_data=True,
                           include_all_writers=True, next_token=0).match(condition="AND", record_types=[sensor_type]).range(start=start, end=end)
            results = self.client.search(query)
            total += results.total_results
            row = [sensor_type, str(results.total_results), str(total)]
            table.append(row)

        print(tabulate(table, headers=[
              "Sensor Type", "Record Count", "Running Total"]))
