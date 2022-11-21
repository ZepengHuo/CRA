from wash.types import Types
import e3db
from e3db.types import Search
import os
import json
import sys
import csv
import uuid


# ===== get qualified users ===================================
# Parse the data_quality_filename from command line
if len(sys.argv) != 5:
    print(f"Incorrect number of arguments. Expected 5 argument, got {len(sys.argv)}.\nUsage: ./downselect_example <data_qaulity_labels.csv>")
    exit(1)
data_quality_filename = sys.argv[1]

# Make sure the filepath is valid
if not os.path.isfile(data_quality_filename):
    print(f"Filename {data_quality_filename} not found")
    exit(1)
        
# Create a list of the desired labels
all_labels = ['committed', 'active', 'intermittent', 'limited-surveys', 'limited-sensors', 'few sensors', 'sparse']
top_users = int(sys.argv[3])-1
desired_labels = all_labels[:top_users]

# desired phone type
desired_phone = sys.argv[4]
        
# Create a set of writer IDs for the desired label
active_users = set()
# Note: You will need to put the actual file name with datestamp here
with open(data_quality_filename, 'r') as file:
    csv_reader = csv.reader(file, dialect='excel')
    # Discard the headers
    next(csv_reader)
    # read each writer-id into a set
    for row in csv_reader:
        if row[1] in desired_labels and row[-1].startswith(desired_phone):
            active_users.add(uuid.UUID(row[0]))
# ===============================================================


if os.path.exists("credentials.json"): 
    client = e3db.Client(json.load(open("credentials.json")))

def download_records(record, client):
    #downloads_path = "./downloads/new_context"
    #downloads_path = "./downloads/new_context_QualifiedUsers"
    downloads_path = sys.argv[2]

    record_id = record.meta.record_id
    user_id = record.meta.user_id
    device_id = record.meta.plain.get('device_id', -1)
    if device_id == -1:
        device_id = record.meta.plain.get('android_id', "NA")
    first_ts = record.meta.plain.get('first_timestamp', "")
    last_ts = record.meta.plain.get('last_timestamp', "")
    orig_fn = record.meta.plain.get("original_file_name", "")

    write_path = os.path.join(
        downloads_path, str(user_id),  str(device_id))

    os.makedirs(write_path, exist_ok=True)

    dest = os.path.join(write_path, '_'.join(
        [first_ts, last_ts, orig_fn]))
    #with open(dest, 'w') as outfile:
    #    json.dump(record, outfile)
    FileMeta = client.read_file(record.meta.record_id, dest)
    
    
#def example_check_fever(self, namespace):
query_items = {}

# Create a query data structure for every day of the week
# where users report "Yes". These uuids are hard-coded in the
# types file. See the spreadsheet for complete data.
# Also demonstrates iterating through the list.

#for survey_uuid in Types.example_fever_every_day:
#    query_items[survey_uuid] = "Yes"
#query_items = {'85be1fd6-3711-42e7-927d-c002c461b9a7': 'Yes'}

# history TBI: 342b43b4-3a0d-4a5c-966c-a64e337e1703
# excercise Mon: 85be1fd6-3711-42e7-927d-c002c461b9a7
#           Tue: 8381785a-78e6-4c52-8525-b716bc706e94
#           Wed: 6215decf-751d-4da0-bdc7-c4071ec43621
#           Thu: 4c5b531f-eab3-4a55-8e59-285945f23629
#           Fri: 88689fb5-365d-4341-9555-e3290216662f
#           Sat: 7b4fe709-4fdb-41eb-885d-fee5ce257a9a
#           Sun: 917bab37-b92f-4d64-8bf8-6d2b50a80039


# activity_yesterday_dict = {
# 'Mon': '25c485c2-dae0-448a-918a-e815b3bdfdc6',
# 'Tue': '670e4888-cad7-4176-8f03-a8945575972f',
# 'Wed': 'c752e9da-0fff-455b-8cd7-f95b23e66f35',
# 'Thu': '21ef22e0-f3dc-46a3-ba56-8ba25eea2f33',
# 'Fri': '4c5b531f-eab3-4a55-8e59-285945f23629',
# 'Sat': '3318ecbe-5719-4730-93e4-8eec664d2817',
# 'Sun': '0309a247-c8a7-4011-8e18-29bdb093b757',
# }

activity_30s_dict = \
{'24e7c071-73d7-41ca-8040-315e20dfe599': 'Please hold the phone in your hand and stay standing (still) for 30 seconds',
 '8e075a12-69ce-4257-a29c-64160cf28f94': 'Please hold the phone in your hand and walk for 30 seconds',
 '8216e14d-7fe3-47b5-87f2-add141709d3f': 'Please hold the phone in your hand and lie down for 30 seconds',
 '9be3cd85-7e95-48b6-9fe6-265a1feffb52': 'Please hold the phone in your hand and sit for 30 seconds',
 #'ff04deb1-cf95-4bca-ba47-9b50d1c8b4f9': 'Did you skip any of the activities',
 #'41b52be7-1b2f-462c-9a10-7fbf627a022d': 'Please tell us why you skip the selected activities',
 '372056d3-afb6-4d17-8b65-c74d069c8a0d': 'Please put the phone in your pocket and stay standing (still) for 30 seconds',
 'c6155ae3-5a4f-445b-b86e-1352acc895cb': 'Please put the phone in your pocket and walk for 30 seconds',
 'cb350c02-66e2-4aaf-b5fe-d2aa02176ae5': 'Please put the phone in your pocket and lie down for 30 seconds',
 '8c42f3fa-aca1-4d02-95f3-7b15e939da42': 'Please put the phone in your pocket and sit for 30 seconds',
 #'b0072c6f-3a5a-48d2-aeb5-749ba66ef8a1': 'Did you skip any of the activities',
 #'84bb8e52-d71c-49c1-a6db-f59da443d0f5': 'Please tell us why you skip the selected activities',
 '1b418ae1-8055-4aa0-8162-ac1c12b05c90': 'Please hold the phone in your hand and sit for 30 seconds',
 'e2db317f-83aa-4177-8987-46a2cb23df5f': 'Please hold the phone in your hand and lie down for 30 seconds',
 '80b15c9d-62f4-4d1f-bb5b-5adaf0b75185': 'Please hold the phone in your hand and walk for 30 seconds',
 'd11ec218-227b-4c9b-9f96-63e13deeb5fc': 'Please hold the phone in your hand and stay standing (still) for 30 seconds',
 #'f4b7d998-0f93-45c0-9942-557ee5f7bf72': 'Did you skip any of the activities',
 #'a55b48d8-5710-4eca-8889-184fa0708b62': 'Please tell us why you skip the selected activities',
 'af63b657-fb29-484d-8a7a-307d5cfce35b': 'Please put the phone in your bag and sit for 30 seconds',
 'e47d04fe-267f-48ce-8af8-3b9ecde85d9d': 'Please put the phone in your bag and lie down for 30 seconds',
 '8a146265-fb30-4675-b7c0-e872638b723b': 'Please put the phone in your bag and walk for 30 seconds',
 '1f27c7cc-8076-434d-a993-847ace9d9fe7': 'Please put the phone in your bag and stay standing (still) for 30 seconds',
 #'ceeb4126-9e4e-4ba6-b39d-126ea46979ed': 'Did you skip any of the activities',
 #'33c9b8ac-24ec-46d8-98b1-38f6c766d774': 'Please tell us why you skip the selected activities',
}

complex_activity_dict = \
{
 '529fe528-8c27-4bf2-95e1-1c80549834f4': 'Bathroom Usage',
 '4522e305-96b7-48bb-a3bf-b149ab16600f': 'Pack a Bag',
 '1edd811b-49b2-4e06-98d2-34dbde8795f1': 'March with a Backpack',
 'f4f706bd-cf94-4140-b712-fd7bd639c4ce': 'Lift and Lower Object',
 '2bb80846-742a-427e-bcd8-9d70bf226382': 'Lift and Carry Load', 
}


query_items = complex_activity_dict


start_index = 0
end_index = len(active_users)
active_users = list(active_users)
index_increment = 20

for key in query_items:
    #for idx in range(start_index, end_index, index_increment):
        #writer_ls = active_users[idx: idx+index_increment]
    query = Search(count=10, include_data=True,
                include_all_writers=True, next_token=0).match(plain={key:'*'}, strategy="WILDCARD", condition='AND'
                                                              #, writers=writer_ls
                                                              )
    #results = self.client.search(query)
    results = client.search(query)
    if len(results) == 0:
        print("Records not found.  Ensure your client has been approved for access")
        #return
    print ("Total results: " + str (results.total_results))
    i = 0 #counter for enumerating
    
    # save first batch
    for record in results:
        print(str(i) + "\t Writer ID: " + str(record.meta.writer_id) + ' ' + str(record.meta.last_modified) + ' ' + complex_activity_dict[key])
        download_records(record, client)
        i = i + 1

    while results.next_token: # Page through results:
        #results = self.client.search(query)
        results = client.search(query)
        
        for record in results:
            # Now do something with each type e.g. fetch more data for that user:
            #print (str(i) + "\t Writer ID: " + str(record.meta.writer_id))
            #print (str(i) + "\t Writer ID: " + str(record.meta.writer_id) + str(record.meta.last_modified) + str(record.meta.plain))
            #if str(record.meta.writer_id) in active_users:

            print(str(i) + "\t Writer ID: " + str(record.meta.writer_id) + ' ' + str(record.meta.last_modified) + ' ' + complex_activity_dict[key])
            download_records(record, client)
            
            i = i + 1

        query.next_token = results.next_token
