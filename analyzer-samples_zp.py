# ---------------------------------------------------------
# Initialization
# ---------------------------------------------------------

import e3db
import json
import requests
from e3db.types import Search
# Required to generate random client id 
import os
import binascii
from datetime import datetime
from tabulate import tabulate
import numpy as np

with open('writerID_ls.npy', 'rb') as f:
    writerID_ls = np.load(f)

def print_records(results):
    # Collect all records in a list
    table = list()
    if len(results) == 0:
        print("Records not found.  Ensure your client has been approved for access")

    for record in results:
        # Combine sensitive info with plaintext meta
        row = dict(record.data)
        row.update(record.meta.plain)

        table.append(row)

    # Print a table of records. (Using tabulate, from https://pypi.org/project/tabulate/)
    #print(table)
    print(tabulate(table, headers="keys"))

def print_record_json(results):
    # Collect all records in a list
    table = list()
    if len(results) == 0:
        print("Records not found.  Ensure your client has been approved for access")

    for record in results:
        # Combine sensitive info with plaintext meta
        row = dict(record)
        

        table.append(row)

    # Print a table of records. (Using tabulate, from https://pypi.org/project/tabulate/)
    print(tabulate(table, headers="keys"))

# If a credentials file exists, use it
# else try and register a client for the user
if os.path.exists("credentials.json"): 
    client = e3db.Client(json.load(open("credentials.json")))
    

  

    # Search for a specific record type
    #query = Search(include_data=True, include_all_writers=True, count=500).match(condition="AND", plain={"type":"a-kry-test-sensor-accelerometer"})
    #results = client.search(query)
    #print_records(results)

    # Search for all record types from a specific user
    #query = Search(include_data=True, include_all_writers=True, count=1000).match(condition="AND", plain={"month":"11","day":"13"}, writers=["9b90d4f0-9cd6-4c94-9ffc-75a729949148"] )
    #query = Search(include_data=True, include_all_writers=True, count=10).match(condition="AND", strategy="WILDCARD", plain={"month":"7", "year":"2021", "original_file_name": "*kry-sensor-survey*"})
    #query = Search(include_data=True, include_all_writers=True, count=10).match(condition="AND", strategy="WILDCARD", plain={"month":"6", "year":"2021"})
    #query = Search(include_data=True, include_all_writers=True, count=1000).match(writers=["1b140a80-9724-4299-a46a-40b9c4e5c882"] )
    
    query = Search(include_data=True, include_all_writers=True, count=1000).match(writers=writerID_ls)
    results = client.search(query)
    print_records(results)


    # Search for all record types from a specific day
    #query = Search(include_data=True, include_all_writers=True, count=500).match(keys=["month"], values=["7"]).match(keys=["year"], values=["2021"])
    #results = client.search(query)
    #print_records(results)


    # Search for all record types from android only
    #query = Search(include_data=True, include_all_writers=True).match(strategy="WILDCARD", plain={"original_file_name": "*-accelerometer*"})
    #results = client.search(query)
    #print_records(results)

    # Search for all record types from gyroscopes only
    #query = Search(include_data=True, include_all_writers=True).match(strategy="WILDCARD", plain={"original_file_name": "*-accelerometer*"})
    #results = client.search(query)
    #print_records(results)

#---

    # Paginating Results
    #query = Search(include_data=True, include_all_writers=True, count=500).match(strategy="WILDCARD", plain={"original_file_name": "*-accelerometer*"})
    #results = client.search(query)

    # Number of results in e3db
    #total_results = results.total_results
    #print(total_results)
    # Return records from this point onwards in next query

    #while results.next_token:
    #    query.next_token = results.next_token
    #    results = client.search(query)
    #    print_records(results)

    
        
    #Write the encrypted files to disk
    if not os.path.isdir('./downloads/'):
        os.mkdir('./downloads/')
    for i, record in enumerate(results):
       
       record_id = record.meta.record_id
       writer_id = record.meta.writer_id
       if not os.path.isdir('./downloads/' + str(writer_id)):
           os.mkdir('./downloads/' + str(writer_id))
       size = record.meta.to_json()
       #print(record.meta.file_meta.to_json())
       #print(record.meta.plain.get("original_file_name","test.txt"))
       dest = "{0}_{1}.{2}".format(record.meta.plain.get("original_file_name","test.txt")[:-4], record.meta.record_id, "txt")
       try:
           FileMeta = client.read_file(record_id, 'downloads/' + str(writer_id) + '/' + dest)
       except e3db.exceptions.APIError:
           print('error')
           print(record.meta.plain.get("original_file_name","test.txt"))



    # Write the file and parse its json...

    # query = Search(include_data=True, include_all_writers=True, count=1).match(strategy="WILDCARD", plain={"original_file_name": "*-accelerometer*"})
    # results = client.search(query)

    # for i, record in enumerate(results):
    #     record_id = record.meta.record_id
    #     print(record.meta.plain.get("original_file_name","test.txt"))
    #     dest = "{1}_{0}".format(record.meta.plain.get("original_file_name","test.txt"), i)
    #     FileMeta = client.read_file(record_id, dest)
    #     with open(dest) as f:
    #         d = json.load(f)
    #         if 'type' not in d:
    #             print_record_json(d[(d.keys()[0])])
    #         if 'type' in d:
    #             print_record_json(d['records'])

else:
    print("No credentials found")