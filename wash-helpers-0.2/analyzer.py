#!/usr/bin/env python3
import secrets
import time

import e3db
from e3db.types import Search
from pprint import pprint
from argparse import ArgumentParser, ArgumentTypeError

from wash.commands import Commands
from wash.types import Types


def user_test(namespace):
    # You can put whatever you want here for running "./analyzer.py test"
    # Edit here directly or in the commands.py file
    wash.user_test()


if __name__ == "__main__":
    print(Types.compliance_message)
    client = Commands.load_client()
    wash = Commands(client)

    # ------- Do some command-ine parsing: ---------
    parser = ArgumentParser(
        description="A scripting framework for WASH performers.")
    parser.set_defaults(func=print("", end=''))
    subparser = parser.add_subparsers(help="Available commands")

    # Test - Use this function to experiment with your own tests
    test_help = "User-defined test."
    test = subparser.add_parser("test", help=test_help, description=test_help)
    test.set_defaults(func=user_test)

    # Smoke test
    smoke_help = "Quick smoke test to query the WASH system."
    smoke = subparser.add_parser(
        "smoke", help=smoke_help, description=smoke_help)
    smoke.set_defaults(func=wash.smoke_test)

    # Sensor test
    sensor_test_help = "Test by querying all of the sensors and counting"
    sensor_test = subparser.add_parser(
        "sensor-test", help=sensor_test_help, description=sensor_test_help)
    sensor_test.set_defaults(func=wash.sensor_test)

    # Query example
    query_help = "Query and print the given number of records e.g. query 10 i-kry-sensor-accelerometer"
    query = subparser.add_parser(
        "query", help=query_help, description=query_help)
    query.add_argument(
        "-d", "--download", help="Download the files into ./downloads", action="store_true")
    query.add_argument(
        "--start-date", help="Provide a query start date, default is 2020-05-01")
    query.add_argument(
        "--end-date", help="Provide a query start date, default is 2020-05-31")
    query.add_argument("number", type=str, help="number of records")
    query.add_argument("--rectype", type=str,
                       help="what type of records to print")
    query.add_argument("-r", "--recfile", type=str,
                       help="File containing a sensors to query for. One per line")
    query.set_defaults(func=wash.query_records)

    # Altitude Weely
    altitude_weekly_help = "Query the number of altitude records and iterate through the weeks."
    altitude_weekly = subparser.add_parser(
        "example-altitude-weekly", help=altitude_weekly_help, description=altitude_weekly_help)
    altitude_weekly.set_defaults(func=wash.example_altitude_weekly)

    # Print a particular record
    record_help = "Print and download a particular record by record ID. (Output file: ./output.txt)"
    record = subparser.add_parser(
        "record", help=record_help, description=record_help)
    record.add_argument(
        "--nodownload", help="Don't download and print the record", action="store_true")
    record.add_argument("record_id", type=str,
                        help="Record ID for this specific record")
    record.set_defaults(func=wash.print_record)

    # List sensors
    listS_help = "List the sensor data types"
    listS = subparser.add_parser(
        "list-sensors", help=listS_help, description=listS_help)
    listS.set_defaults(func=wash.list_sensors)

    args = parser.parse_args()
    if not args.func:
        parser.print_help()
    else:
        args.func(args)
