# wash-helpers

This repository contains a simple command-line utility and some helper
functions in Python. The purpose of this is to give TA2 performers a
repeatable way to share best practices for querying and parsing WASH
data.

Feel free to edit the source files to perform your own commands and
analysis.

Please clone this repository and issue pull requests to add features
'that will be useful to others.

These are examples only. More complete documentation is available at the [Tozny Python repository](https://github.com/tozny/e3db-python).

# Compliance

Data accessed from this system contains CONTROLLED UNCLASSIFIED
INFORMATION (CUI).  Please contact the system Authorizer
(bbracken@cra.com) if you have any questions.

# Requirements

Get a credentials.json file from the portal and put it in this directory or in ```~/.tozny/wash-fedramp/e3db.json```.

```
pip3 install -r requirements.txt
```

or

```
pip3 install e3db
pip3 install tabulate
```

# Examples:

```./wash-helper.py help```
To print the latest help text.


```./wash-helper.py query --help```
To print the detailed help text for query.

```./wash-helper.py smoke```
To do basic testing of your configuration.

This command queries 5 records of the given type:
```
./wash-helper.py query 5 -t a-kry-sensor-accelerometer

Querying 5 records of type: a-kry-sensor-accelerometer
Total results: 4830
android_id                              day    fileSize    first_timestamp
------------------------------------  -----  ----------  -----------------
53543df5-ae0c-46fa-81d3-4845e819e315      9      243359      1589065420263
53543df5-ae0c-46fa-81d3-4845e819e315     12       54532      1589338848597
53543df5-ae0c-46fa-81d3-4845e819e315     15       91240      1589515290796
53543df5-ae0c-46fa-81d3-4845e819e315     11      543494      1589174754033
53543df5-ae0c-46fa-81d3-4845e819e315     12       15381      1589337341380
```

This command queries 5 records from the set in the file example-sensors.txt:
```./wash-helper.py query 5 -f example-sensors.txt```

Query during the month of April and download the resulting files.

```
./wash-helper.py query --download --end-date=2020-04-30 --start-date=2020-04-01 5 a-kry-sensor-accelerometer
Querying 5 records of type: a-kry-sensor-accelerometer from 2020-04-01 00:00:00 to 2020-04-30 00:00:00
Total results: 39
android_id                              day    fileSize    first_timestamp
------------------------------------  -----  ----------  -----------------
1092803f-b7b7-4c55-9ca3-008337eb5365     28       90633      1588050862702
1092803f-b7b7-4c55-9ca3-008337eb5365     26       90436      1587901528272
1092803f-b7b7-4c55-9ca3-008337eb5365     28       91119      1588050257227
1092803f-b7b7-4c55-9ca3-008337eb5365     28       15309      1588038073015
1092803f-b7b7-4c55-9ca3-008337eb5365     29       15333      1588177469229
Downloading files into ./downloads
```


# In the Code

The true purpose is to give you code examples to modify to suit your
needs.  For example in the commands.py file, a function to correlate
answers to a survey question and fetch the related user IDs:

```
    def example_check_fever(self, namespace):
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
        print ("Total results: " + str (results.total_results))
        i = 0 #counter for enumerating

        while results.next_token: # Page through results:
            results = self.client.search(query)

            for record in results:
                # Now do something with each type e.g. fetch more data for that user:
                print (str(i) + "\t Writer ID: " + str(record.meta.writer_id))
                i = i + 1

            query.next_token = results.next_token
```
