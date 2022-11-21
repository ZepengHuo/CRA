#!/usr/bin/env python3

"""
This script will download the csv files that describe the data quality of study
participants that are not bad-actors.

Usage:
	./data_quality.py

Output:
	File 1: data_quality_labels.csv - gives a quality label for each writer ID
	File 2: data_quality_thresholds.csv - gives the thresholds used to define each quality label
"""

from e3db.types import Search
from wash.commands import Commands
from wash.types import Types

DATA_QUALITY_RECORD_TYPE = 'dataquality'
THRESHOLDS_RECORD_TYPE = 'dataqualitythresholds'

def get_latest_record_of_type(client, record_type, filename):
	# Search for all records of a given type shared with this client
	query = Search(include_data=True, include_all_writers=True).match(record_types=[record_type])
	query_result = client.search(query)

	# Short circuit with error message if no records found
	if(len(query_result) < 1):
		print(f"Error, unable to locate any files of record type {record_type} shared with {client.client_id}")
		return

	# Only get the data from the latest version
	for i, record in enumerate(query_result):
		if i == 0:
			latest_record = record
		else:
			if record.meta.created > latest_record.meta.created:
				latest_record = record

	# Parse date for filename
	date = latest_record.meta.created
	dest = f"{date.year}{date.month}{date.day}_{filename}.csv"

	# Fetch and save file
	client.read_file(latest_record.meta.record_id, dest)
	print(f"Saving record ID: {latest_record.meta.record_id} to file {dest}")


def main():
	print(Types.compliance_message)
	try:
		client = Commands.load_client()
	except Exception as ex:
		print(f"Unable to create client. Error: {ex}")
		exit()

	# Query for all records shared with you that are of type dataquality
	# Saves the latest to file in a local directory
	try:
		get_latest_record_of_type(client, DATA_QUALITY_RECORD_TYPE, 'data_quality_labels')
	except Exception as ex:
		print(f"Error getting latest data quality labels file. Error: {ex}")

	# Query for all records shared with you that are of type dataqualitythresholds
	# Saves the latest to file in a local directory
	try:
		get_latest_record_of_type(client, THRESHOLDS_RECORD_TYPE, 'data_quality_thresholds')
	except Exception as ex:
		print(f"Error getting latest data quality thresholds file. Error: {ex}")


if __name__ == "__main__":
	main()

