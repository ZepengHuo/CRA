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


#dict_file = 'json_data_i_dict_formatted.p'
dict_file = 'json_data_a_dict_formatted.p'

with open(dict_file, 'rb') as f:
    json_data_dict_formatted = pickle.load(f)


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


for writerID in json_data_dict_formatted:
    activity_ls = json_data_dict_formatted[writerID].keys()
    for activity in activity_ls:
        for trial in json_data_dict_formatted[writerID][activity]:
            dateTime = datetime.datetime.fromtimestamp(trial[0])
            buffer_len = 3600
            print((dateTime), trial[0] - buffer_len, trial[1] + buffer_len)
            
            
            try:
                #if writerID not in existing_writer_ls:
                if os.path.exists("credentials.json"): 
                    client = e3db.Client(json.load(open("credentials.json")))
                    
                    
                    
                    #query = Search(include_data=True, include_all_writers=True, count=10).match(condition="AND", strategy="WILDCARD", plain={"month":"6", "year":"2021"})
                    query = Search(include_data=True, include_all_writers=True, count=1000) \
                            .match(writers=[writerID], condition="AND", strategy="WILDCARD", plain={"original_file_name": "i-kry-sensor-*"}) \
                            .range(start=int(trial[0] - buffer_len), end=int(trial[1] + buffer_len)) 

                            #.match(condition="AND", strategy="WILDCARD", plain={"month":str(dateTime.month), 
                            #                                                    "year":str(dateTime.year), 
                            #                                                    'day':str(dateTime.day),
                            #                                                    "original_file_name": "i-kry-sensor-*"})
                    results = client.search(query)
                    print_records(results)
                    
                    # Write the encrypted files to disk for the first batch
                    if not os.path.isdir('./downloads/newSensor/'):
                        os.mkdir('./downloads/newSensor/')
                    for i, record in enumerate(results):
                    
                        record_id = record.meta.record_id
                        writer_id = record.meta.writer_id
                        if not os.path.isdir('./downloads/newSensor/' + str(writer_id)):
                            os.mkdir('./downloads/newSensor/' + str(writer_id))
                        size = record.meta.to_json()
                        #print(record.meta.file_meta.to_json())
                        #print(record.meta.plain.get("original_file_name","test.txt"))
                        dest = "{0}_{1}.{2}".format(record.meta.plain.get("original_file_name","test.txt")[:-4], record.meta.record_id, "txt")
                        try:
                            FileMeta = client.read_file(record_id, 'downloads/newSensor/' + str(writer_id) + '/' + dest)
                        except e3db.exceptions.APIError:
                            print('error')
                            print(record.meta.plain.get("original_file_name","test.txt"))
                        
                    '''
                    while results.next_token: # Page through results:
                        results = client.search(query)
                        #Write the encrypted files to disk
                        if not os.path.isdir('./downloads/newSensor/'):
                            os.mkdir('./downloads/newSensor/')
                        for i, record in enumerate(results):
                        
                            record_id = record.meta.record_id
                            writer_id = record.meta.writer_id
                            if not os.path.isdir('./downloads/newSensor/' + str(writer_id)):
                                os.mkdir('./downloads/newSensor/' + str(writer_id))
                            size = record.meta.to_json()
                            #print(record.meta.file_meta.to_json())
                            #print(record.meta.plain.get("original_file_name","test.txt"))
                            dest = "{0}_{1}.{2}".format(record.meta.plain.get("original_file_name","test.txt")[:-4], record.meta.record_id, "txt")
                            try:
                                FileMeta = client.read_file(record_id, 'downloads/newSensor/' + str(writer_id) + '/' + dest)
                            except e3db.exceptions.APIError:
                                print('error')
                                print(record.meta.plain.get("original_file_name","test.txt"))
                            
                        
                        query.next_token = results.next_token
                    '''
                        
                else:
                    print("No credentials found")
            except:
                continue