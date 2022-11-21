# %%
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
import pickle
import datetime

# %%
with open('json_data_i_dict_formatted.p', 'rb') as f:
    json_data_i_dict_formatted = pickle.load(f)


existing_writer_ls = os.listdir('./downloads')

np_file = 'writerID_label30s.npy'
with open(np_file, 'rb') as f:
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

# %%
writerID_ls = []
for writerID in json_data_i_dict_formatted:
    writerID_ls.append(writerID)

# %%
#writerID = writerID_ls[2]
#print(writerID)

for writerID in json_data_i_dict_formatted:
    activity_ls = json_data_i_dict_formatted[writerID].keys()
    for activity in activity_ls:
        for trial in json_data_i_dict_formatted[writerID][activity]:
            dateTime = datetime.datetime.fromtimestamp(trial[0])
            buffer_len = 10000
            startTime_buffed = int(trial[0] - buffer_len)
            endTime_buffed = int(trial[1] + buffer_len)
            startTime_buffed_str = str(startTime_buffed)[:6] + '*'
            endTime_buffed_str = str(endTime_buffed)[:6] + '*'
            middleNum = int(startTime_buffed_str[5]) + 1
            middleTime_buffed_str = startTime_buffed_str[:5] + str(middleNum) + '*'


            if os.path.exists("credentials.json"): 
                client = e3db.Client(json.load(open("credentials.json")))




                query = Search(include_data=True, include_all_writers=True, count=1000) \
                        .match(writers=[writerID], condition="AND", strategy="WILDCARD", 
                               plain={"original_file_name": "i-kry-sensor-*", 
                                     'first_timestamp': startTime_buffed_str}) \
                        .match(writers=[writerID], condition="AND", strategy="WILDCARD", 
                               plain={"original_file_name": "i-kry-sensor-*", 
                                     'last_timestamp': endTime_buffed_str}) \
                        .match(writers=[writerID], condition="AND", strategy="WILDCARD", 
                               plain={"original_file_name": "i-kry-sensor-*", 
                                     'first_timestamp': middleTime_buffed_str}) \
                        .match(writers=[writerID], condition="AND", strategy="WILDCARD", 
                               plain={"original_file_name": "i-kry-sensor-*", 
                                     'last_timestamp': middleTime_buffed_str}) \

                        #.range(start=int(trial[0] - buffer_len), end=int(trial[1] + buffer_len)) 
                        #.exclude(condition="AND", strategy="WILDCARD", plain={"original_file_name": "i-kry-sensor-survey*"}) \



                results = client.search(query)
                #print_records(results)

                # Write the encrypted files to disk for the first batch
                if not os.path.isdir('./downloads/trial/'):
                    os.mkdir('./downloads/trial/')
                for i, record in enumerate(results):

                    record_id = record.meta.record_id
                    writer_id = record.meta.writer_id
                    created = int(record.meta.created.timestamp())
                    last_modified = int(record.meta.last_modified.timestamp())
                    filename = record.meta.plain.get("original_file_name","test.txt")[:-4]
                    first_timestamp = int(float(record.meta.plain['first_timestamp']))
                    last_timestamp = int(float(record.meta.plain['last_timestamp']))


                    if first_timestamp < int(trial[0]) and int(trial[1]) < last_timestamp:
                        print(filename)

                        ####### write down to folder
                        if not os.path.isdir('./downloads/trial/' + str(writer_id)):
                            os.mkdir('./downloads/trial/' + str(writer_id))
                        size = record.meta.to_json()
                        dest = "{0}_{1}.{2}".format(record.meta.plain.get("original_file_name","test.txt")[:-4], record.meta.record_id, "txt")
                        try:
                            FileMeta = client.read_file(record_id, 'downloads/trial/' + str(writer_id) + '/' + dest)
                        except e3db.exceptions.APIError:
                            print('error')
                            print(record.meta.plain.get("original_file_name","test.txt"))


                        ####### go to folder to check
                        '''
                        sensor_key = dest.split('_')[0]
                        with open('downloads/trial/' + str(writer_id) + '/' + dest) as f:
                            js = json.load(f)
                            timeseries_ls = js[sensor_key]
                            feature_ls = []
                            for timestamp in timeseries_ls:
                                if int(trial[0]) < int(float(timestamp['timestamp'])) < int(trial[1]):
                                    feature_ls = list(timestamp.keys())
                                    feature_ls.remove('timestamp')
                            if feature_ls:
                                print(feature_ls)
                        '''
            else:
                print("No credentials found")