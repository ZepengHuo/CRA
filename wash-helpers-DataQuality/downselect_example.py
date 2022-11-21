#!/usr/bin/env python3

"""
This script provides an example for downselecting data based on data quality labels for writer IDs.
In order to use this script you can downloaded the current <datestamp>_data_quality_labels.csv file
using the data_quality.py script located in the WASH-HELPERS repository. Use that filename as an argument
to this script. For example ./downselect_example.py 20211012_data_quality_labels.csv

Requires placement in WASH-HELPERS directory
Credentials must be stored at ~/.tozny/wash-fedramp/e3db.json

NOTE: The will need to update the constant DATA_QUALITY_FILENAME with the current version of this file

Usage ./downsselect_example.py <Filepath to data labels csv>

The expected output is a list of record_ids printed to the console.
"""

import csv
import sys
import os.path
from wash.commands import QueryIterate, Commands, Search

def main():

    # Parse the data_quality_filename from command line
    if len(sys.argv) != 2:
        print(f"Incorrect number of arguments. Expected 1 argument, got len(sys.arg).\nUsage: ./downselect_example <data_qaulity_labels.csv>")
        exit(1)
    data_quality_filename = sys.argv[1]

    # Make sure the filepath is valid
    if not os.path.isfile(data_quality_filename):
        print(f"Filename {data_quality_filename} not found")
        exit(1)

    # Load a client using stored credentials at ~/.tozny/wash-fedramp/e3db.json
    client = Commands.load_client()

    # Create a query for records. In this case we are searching for accelerometer
    # data between 4/12/2020 and 4/14/2020
    start = Commands.fromisoformat('2020-04-12')
    end = Commands.fromisoformat('2020-04-14')
    query = Search(include_data=False,
                      include_all_writers=True, next_token=0).match(condition="AND", record_types=["a-kry-sensor-accelerometer"]).range(start=start, end=end)

    # Making use of the Wash-Helpers QueryIterator to page all results from the query
    records = QueryIterate(client, query)

    # Throw an error if no records found
    records.raiseIfNone()

    # Place each writer ID into a set
    query_set = set()
    for record in records:
        query_set.add(str(record.meta.writer_id))

    # Create a list of the desired labels
    desired_labels = ['committed', 'active']

    # Create a set of writer IDs for the desired label
    active_users = set()
    # Note: You will need to put the actual file name with datestamp here
    with open(data_quality_filename, 'r') as file:
        csv_reader = csv.reader(file, dialect='excel')
        # Discard the headers
        next(csv_reader)
        # read each writer-id into a set
        for row in csv_reader:
            if row[1] in desired_labels:
                active_users.add(row[0])

    # Take the intersection of the two sets
    final_set = query_set.intersection(active_users)

    # Now we can filter data using the set of writer IDs
    # In this case we are printing the record IDs for this query to the console
    query = Search(include_data=False,
                   include_all_writers=True, next_token=0).match(condition="AND", record_types=["a-kry-sensor-accelerometer"]).range(start=start, end=end)
    records = QueryIterate(client, query)
    for record in records:
        if str(record.meta.writer_id) in final_set:
            print(record.meta.record_id)


if __name__ == "__main__":
	main()
