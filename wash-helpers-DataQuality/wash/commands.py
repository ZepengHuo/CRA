import e3db
import os
import sys
import uuid

from datetime import datetime
from datetime import timedelta
from e3db.types import Search
from itertools import groupby
from json import load
from operator import itemgetter
from tabulate import tabulate
from wash.parse import Parse
from wash.query_iterate import QueryIterate
from wash.types import Types

MAX_SEARCH_PAGE_DEPTH=10000

class Commands:
    downloads_path = "./downloads"
    example_survey_record_id = "47f4c1bd-f308-4c7a-ac80-bd0622fcf767"
    example_accel_record_id = "d2ebdf48-af0e-41cf-8b3e-b2dbc3aa5150"

    def __init__(self, c):
        self.client = c
        self.total_downloaded = 0
        self.record_ids = []
        self.record_id_file = open(
            "record_id_file.txt", 'a+')  # mild record keeping
        self.error_id_file = open(
            "download_error_record_ids_file.txt", 'a+')  # mild record keeping
        # load the previously gotten record UUIDs so we don't fetch again
        # seek to the beginning for a read of the whole file.
        self.record_id_file.seek(0)
        # Read in Bad Actor Writer Ids Provided by Analyst
        with open('bad_actors_writer_ids.txt', 'r') as self.bad_actors_file:
            self.bad_actors_ids = [uuid.UUID(x.strip("'\n,"))
                                   for x in self.bad_actors_file.readlines()]
        self.record_ids = [uuid.UUID(x.strip())
                           for x in self.record_id_file.readlines()]

    def __del__(self):
        # ensure the file closes at the end
        self.record_id_file.close()
        self.bad_actors_file.close()

# ------------------------ Your Test Here ---------------------------
    def user_test(self):
        print("User test here.")

# --------------------------- Commands -------------------------------

    def smoke_test(self, namespace):
        print("Able to link into the WASH library.")
        print("Config file location: " + Commands.config_location())

        print("Querying a record we know should exist.")
        accel_id = "93c17a36-21b9-4592-9166-8dd4b0317e79"
        FileMeta = self.client.read_file(accel_id, "sensor-output.txt")
        print("Done fetching. Reading file.")

        with open("sensor-output.txt", "r") as f:
            json_version = load(f)
        print("JSON version: " + str(json_version))
        expected_startTime = 1589957453888
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
        if namespace.window:
            window = namespace.window
        else:
            window = 5

        if namespace.align:
            # split iPhone and android
            for _, rt in groupby(sorted(rec_types), key=itemgetter(0)):
                self.query_corresponding(namespace.number, list(rt),
                                         namespace.download, start, end,
                                         window=namespace.window, max_records=namespace.max_records)
        else:
            self.print_records_type(namespace.number, rec_types,
                                    namespace.download, start, end, page=namespace.page, max_records=namespace.max_records, interval_minutes=namespace.interval_minutes)

    def list_sensors(self, namespace):
        for sensor in sorted(Types.all_sensors()):
            print(sensor)

    def user_data(self, namespace):
        if namespace.userfile:
            writer_ids = [r.strip()
                          for r in open(namespace.userfile).readlines()]

            for w in writer_ids:
                self.user_data_single(w)

        else:
            self.user_data_single(namespace.writer_id)

    def user_data_single(self, writer_id):
        print("Downloading data for: " + writer_id)
        query = Search(include_data=True,
                       include_all_writers=True, next_token=0).match(writers=[writer_id])
        q = QueryIterate(self.client, query)
        if (len(q) <= 0):
            print("Given uid is not writer_id, trying android_id and device_id")
            query = Search(include_data=True,
                           include_all_writers=True, next_token=0).match(plain={"android_id": writer_id,
                                                                                "device_id": writer_id})
            q = QueryIterate(self.client, query)
        q.raiseIfNone()  # Throw error if no results
        self.download_records(q)

    def example_android_accel_parse(self, namespace):
        query = Search(count=1, include_data=True,
                       include_all_writers=True, next_token=0).match(record_types=["a-kry-sensor-accelerometer"])
        q = QueryIterate(self.client, query, max=1)
        q.raiseIfNone()  # Throw error if no results
        for record in q:  # Should only be one
            self.client.read_file(
                record.meta.record_id, "output.txt")
            with open("output.txt", "r") as f:
                parse = Parse()
                data = parse.parse_android_accelerometer(f)
                parse.print_android_accelerometer(data)

    def example_iterate_baseline(self, namespace):
        gender_q_id = "f9b45d1b-e2a6-41bb-bc24-1752bfb3b225"
        hand_q_id = "3f364a9b-a6cf-49ef-b095-40d028ad9544"

        query = Search(count=200, include_data=False,
                       include_all_writers=True, next_token=0).match(
                           strategy="WILDCARD",
                           plain={hand_q_id: "*t"})  # Example wildcard for handedness ending in 't'
        q = QueryIterate(self.client, query, max=503)
        q.raiseIfNone()  # throw error if no results
        print("Total results: " + str(q.total_results))
        print("Has records: " + str(q.has_data))
        i = 0
        for record in q:
            gender = record.meta.plain.get(gender_q_id, "NONE")
            hand = record.meta.plain.get(hand_q_id, "NONE")

            print(str(i) + "\t Writer ID:Record ID: " + str(record.meta.writer_id)
                  + str(record.meta.record_id)
                  + "---:-Gender: " + gender + " Hand: " + hand)
            i += 1

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
        query_items = {}

        # Create a query data structure for every day of the week
        # where users report "Yes". These uuids are hard-coded in the
        # types file. See the spreadsheet for complete data.
        # Also demonstrates iterating through the list.

        for survey_uuid in Types.example_fever_every_day:
            query_items[survey_uuid] = "Yes"

        query = Search(count=50, include_data=True,
                       include_all_writers=True, next_token=0).match(plain=query_items)
        q = QueryIterate(self.client, query, max=200)
        q.raiseIfNone()  # Throw error if no results
        print("Total results: " + str(q.total_results))

        for record in q:
            # Now do something with each type e.g. fetch more data for that user:
            print("\t Writer ID:Record ID: " +
                  str(record.meta.writer_id) + ":" + str(record.meta.record_id))

    def query_corresponding(self, number, rectype, do_download, start, end,
                            next_token=0, window=5, max_records=None):
        """
        Query for all record for the first rectype passed in. Narrow the window for start/end time to +/1 the window variable.
        Query again, for each sensor individually using the given user_id from the first query and the narrowed time range.
        Repeat until the max_records is reached. Creates a collection id for the result to easily correlate them
        together for post-processing and adds it to the file structure.
            ./downloads/[user_id]/[device_id]/[collect_id]/[rec_id]_[first_ts]_[last_ts]_[orig_filename]

        :param number - int
            max number of records to query for in a single call

        :param rectype - list, string
            record_types to query for. Should be only Android or only iPhone

        :param do_download - bool
            download the records

        :param start - datetime object
            overarching start time to query against for records

        :param end - datetime object
            overarching end time to query against

        :param next_token - int
            next record to query for. here for recursion

        :param window - int
            Number of minutes to +/- the start time of the first queried record
            Default: 5

        :param max_record - int
            maximum number of records to query for

        :return N/A
        """

        # verfiy input
        if isinstance(rectype, str):
            rectype = [rectype]

        # ensure sensors are of the same type
        device_type = rectype[0][0]  # first letter indictates android/iphone
        # sanity check
        # this should be handled outside the function if passed sensors for multiple device are passed
        rectype = [s for s in rectype if s[0] == device_type]

        # query for records of one sensor within a time window
        query = Search(count=number, include_data=False,
                       include_all_writers=True, next_token=next_token).match(condition="AND", record_types=[rectype[0]]).range(start=start, end=end)
        results = self.client.search(query)
        print("Total results: " + str(results.total_results))

        while results.next_token:
            # First time through call is redundant but not incorrect
            results = self.client.search(query)
            for record in results:
                user_id = record.meta.user_id
                # query again for sensors within the same window +- 1 hour
                first_ts = Commands.convert_timestamp(
                    record.meta.plain.get('first_timestamp', ""))
                last_ts = Commands.convert_timestamp(
                    record.meta.plain.get('last_timestamp', ""))
                # create the search window
                start = first_ts - timedelta(minutes=window)
                end = first_ts + timedelta(minutes=window)
                for rec in rectype:
                    sub_query = Search(count=number, include_data=True,
                                       include_all_writers=True, next_token=next_token).match(condition="AND",
                                                                                              users=[user_id], record_types=[rec]).range(start=start, end=end)

                    sub_results = self.client.search(sub_query)
                    if not max_records:
                        max_records = results.total_results
                    print("\tTotal sub-results: " +
                          str(sub_results.total_results))
                    if sub_results.next_token >= number:
                        print(
                            "Too many records returned in the window. Consider narrowing")
                    else:
                        # Only print records if we got a non empty page of search results
                        # otherwise only stop when the next token is 0
                        if (len(sub_results) != 0):
                            self.print_records(sub_results)
                            if (do_download):
                                print("Downloading files into ./downloads")
                                self.download_records(
                                    sub_results, collect_id=first_ts)
                            self.total_downloaded += int(
                                sub_results.total_results)
            query.next_token = results.next_token
            if self.total_downloaded > max_records:
                break

    def traumatic_brain_injury(self, namespace):
        query = Search(include_data=True,
                       include_all_writers=True, next_token=0).match(plain=Types.traumatic_brain_injury_questions_to_response)
        q = QueryIterate(self.client, query)
        q.raiseIfNone()  # Throw error if no results
        print("Total Amount of Surveys With Traumatic Brain Injuries: " +
              str(q.total_results))
        # Stores non duplicate Users
        users = []
        print("All Surveys With Traumatic Brain Injuries are being written to file: traumatic_brain_injuries.txt ")
        traumatic_brain_injuries_file = open(
            'traumatic_brain_injuries.txt', 'w')
        for record in q:
            # Ignore Bad Actors writer ID
            if str(record.meta.writer_id) not in self.bad_actors_ids:
                # Gives TA2s all the records with traumatic brain injuries
                print("\tWriter ID:" + str(record.meta.writer_id) +
                      "\tRecord ID: " + str(record.meta.record_id), file=traumatic_brain_injuries_file)
                if str(record.meta.writer_id) not in users:
                    users.append(str(record.meta.writer_id))
        traumatic_brain_injuries_file.close()
        # Gives the TA2s A list of users with traumatic brain injuries
        print("\nUsers WriterIDs with Traumatic Brain Injuries Written to File: traumatic_brain_injury_writer_ids.txt ")
        with open('traumatic_brain_injury_writer_ids.txt', 'w') as traumatic_brain_injury_writer_ids_file:
            print("\t Writer IDs: " + str(users),
                  file=traumatic_brain_injury_writer_ids_file)
        traumatic_brain_injury_writer_ids_file.close()

# --------------------------- Helpers -------------------------------
    @ staticmethod
    def convert_timestamp(ts):
        """
        Converts a timestamp from the DB to a datetime object and returns it

        :parma ts - string, int, or float
            timestamp from the database. Will convert a to a float

        :return datetime.datetime object
        """
        try:
            return datetime.fromtimestamp(float(ts))
        except ValueError:  # handle android timestamps
            return datetime.fromtimestamp(float(ts)/1000)

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

    def download_records(self, results, collect_id=None):
        if len(results) == 0:
            print("Records not found.  Ensure your client has been approved for access")

        count = 1
        total = len(results)

        for record in results:
            record_id = record.meta.record_id
            print("Checking: " + str(count) + "/" + str(total), end='')
            count = count + 1

            if record_id not in self.record_ids:  # no need to re-download

                user_id = record.meta.user_id
                print(" (downloading writer_id: " + str(user_id) + ")")
                device_id = record.meta.plain.get('device_id', -1)
                if device_id == -1:
                    device_id = record.meta.plain.get('android_id', "NA")
                first_ts = record.meta.plain.get('first_timestamp', "")
                last_ts = record.meta.plain.get('last_timestamp', "")
                orig_fn = record.meta.plain.get("original_file_name", "")

                write_path = os.path.join(
                    self.downloads_path, str(user_id),  str(device_id))
                if collect_id:
                    write_path = os.path.join(write_path, str(collect_id))
                os.makedirs(write_path, exist_ok=True)

                dest = os.path.join(write_path, '_'.join(
                    [str(record_id), first_ts, last_ts, orig_fn]))
                try:
                    FileMeta = self.client.read_file(
                        record.meta.record_id, dest)
                    self.record_ids.append(record_id)
                    self.record_id_file.write(str(record_id) + "\n")
                except KeyboardInterrupt:
                    exit()
                except:
                    print("Error with record ID: " +
                          str(record.meta.record_id))
                    self.error_id_file.write(str(record_id) + "\n")
            else:
                print(" (skipped)")
    def print_records_type(self, number, rectype, do_download, start, end, next_token=0, page=True, max_records=10000, interval_minutes=360):
        if (self.total_downloaded >= max_records):
            return
        if (rectype == None):
            exit("Cannot query on None records type.")
        print("Querying " + str(number) + " records of type: " +
              str(rectype) + " from " + str(start) + " to " + str(end))
        if isinstance(rectype, str):
            rectype = [rectype]
        query = Search(count=number, include_data=True,
                       include_all_writers=True, next_token=next_token).match(condition="OR", record_types=rectype).range(start=start, end=end)

        results = self.client.search(query)
        new_next = results.next_token
        print("Total results: " + str(results.total_results))
        if (results.total_results) > MAX_SEARCH_PAGE_DEPTH:
            if (end - start <= timedelta(minutes=interval_minutes)):
                interval_minutes = int (interval_minutes / 2)
                if interval_minutes <= 0:
                    return
            print(f"More than {MAX_SEARCH_PAGE_DEPTH} found within timeframe, starting sub searches from start-date + {interval_minutes} minutes to end-date and start-date + {interval_minutes} minutes to end-date")
            self.print_records_type(number, rectype, do_download, start, start + timedelta(minutes=interval_minutes), 0, page, max_records, interval_minutes)
            self.print_records_type(number, rectype, do_download, start + timedelta(minutes=interval_minutes), end, 0, page, max_records, interval_minutes)
            return
        # Only print records if we got a non empty page of search results
        # otherwise only stop when all pages have been retrieved or paging is disabled
        if (len(results) != 0):
            self.print_records(results)
            if (do_download):
                print("Downloading files into ./downloads")
                self.download_records(results)
            self.total_downloaded += int(number)
        else:
            return
        # Basically always the case, users want their number of records, they don't
        # care if the client and server have to do a pagination dance
        if page:
            # If we've downloaded less then the total number of results
            if self.total_downloaded <= results.total_results:
                # Recursively grab the next page using the new next token
                self.print_records_type(
                    number, rectype, do_download, start, end, new_next, page,max_records, interval_minutes)

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
