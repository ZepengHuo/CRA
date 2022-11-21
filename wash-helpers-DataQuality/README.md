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
INFORMATION (CUI). Please contact the system Authorizer
(bbracken@cra.com) if you have any questions.

# Requirements

Get a credentials.json file from the portal and put it in this directory or in `~/.tozny/wash-fedramp/e3db.json`.

The contents of this file should look like

```json
{
  "api_key_id": "52d9beb5d4d4ee08f031054e902c4cbe5d376957999880ba8563e46a16606123",
  "api_secret": "c74af5780edfeafcf71453147c3d3ea758624fb7885e63d3fdcb3b96b6800b75",
  "api_url": "https://api.fedramp.e3db.com",
  "client_email": "",
  "client_id": "8835c590-0c94-4ebd-8e2f-c91572c8a2d4",
  "private_key": "nt3UAy9KGmCiYHXUA3p9FA11nRr8kXXTZ_G7Yz-bNqs",
  "private_signing_key": "O6rHzujwBKwdLywVwfpv_DZJNtnhOcrs-pE0NB5XMkBGu_CYXnEq_G2IWgSgN0nM1fs5UrgyCvhD4mW_vZPIPg",
  "public_key": "0N0ttm80tkNuAtrOY_K8NMegS-_cgWESlb0CWeaOsCM",
  "public_signing_key": "RrvwmF5xKvxtiFoEoDdJzNX7OVK4Mgr4Q-Jlv72TyD4",
  "version": 2
}
```

Get a bad actor file from the portal and put it in this directory.

The contents of this file should look like

```
'e66b251d-f136-4dc6-938c-741157fa83cc',
'43347e62-2549-4834-8a58-a0775413b07f',
'df9755cc-bcdf-4db4-9b42-b76d14e4fbb5',
'6eee687c-e2fe-484d-8864-103fef88640e',
'5c62b153-b4be-4c56-b324-b8e32d6a8f49',
'7d84d258-b678-46b9-8128-1e5c33aaf68c',
'28d4b390-e4b2-4078-8a31-330b2cbcfa83',
'4666f234-790a-4e50-bb5a-d367837f0d93',
'8d5eee64-5c19-4349-9111-f6989fafc62e',
'3dc44c19-7a99-46f0-9235-ddd21a62bd5e',
'2d563db1-5f22-40f5-b4f7-8ab305904c4a',
'ebd4ba12-d832-432b-b832-3ee201bee34e',
'003038f6-b5a9-42d7-8756-5791c46783ec',
```

Then install all python dependencies used by the helpers

```
pip3 install -r requirements.txt
```

or

```
pip3 install e3db
pip3 install tabulate
```

# Examples:

`./wash-helper.py help`
To print the latest help text.

`./wash-helper.py query --help`
To print the detailed help text for query.

`./wash-helper.py smoke`
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

This command downloads all the files for a given writer_id:
`./wash-helper.py user-data --writer_id=12345`

This command downloads all the files for all the users in a file of writer_ids:
`./wash-helper.py user-data --userfile=writers.txt`

This command queries 5 records from the set in the file example-sensors.txt:
`./wash-helper.py query 5 -f example-sensors.txt`

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

The below command shows how to query for an arbitrary max number of records of a certain type over a given time range
using the -m flag to specify the max number of records to retrieve and the -p flag to grab the records in chunks of 1000 (for high number of -m chunk size should always be the max possible - 1000)

```
./wash-helper.py query --download --end-date=2021-04-30 --start-date=2020-04-01 1000 -m 1000000 -t a-kry-sensor-accelerometer -p
```

By default the above command will (if more than 10000 total results) divide the original time range into sub searches from start-date + interval-minutes to end-date and start-date + interval minutes to end-date, defaulting to 360 minutes. You can specify a different interval using the -i flag

```
 ./wash-helper.py query --download --end-date=2021-05-30 --start-date=2021-05-01 1000 -m 12000 -t a-kry-sensor-audio-feature -p -i 720
 ```

This command queries all records related to traumatic brain injury and creates a new file for the writer_ids:
`./wash-helper.py traumatic_brain_injury `

# In the Code

The true purpose is to give you code examples to modify to suit your
needs. For example in the commands.py file, a function to correlate
answers to a survey question and fetch the related user IDs:

```python
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
        q.raiseIfNone() # Throw error if no results
        print("Total results: " + str(q.total_results))

        for record in q:
            # Now do something with each type e.g. fetch more data for that user:
            print("\t Writer ID:Record ID: " + str(record.meta.writer_id) + ":" + str(record.meta.record_id))
```
**Note: The QueryIterate helper can only be consumed once.** If you wish to iterate across the resulting list of records more than once, and the list is not too large, you can copy the QueryIterator into a list. Otherwise you must create a new QueryIterator.
```python
records = list(q)
for record in records:
    # Now do something else
```
# Data Quality Labels

We have a script which will facilitate downloading a .csv file that contains a data quality label for each unique writer ID associated with data collected and stored in TozStore for presumed good-actors.
Once credentials have been saved as outlined in the requirements section of this README, you can run the script as follows:
```bash
./data_quality.py
```
The output of this file will be two files:
1. **\<datestamp>_data_quality_labels.csv** - This file gives a quality label for each writer ID as well as the raw data used in the categorization process described above.
2. **\<datestamp>_data_quality_thresholds.csv** - This file gives the thresholds used to define each label for the downloaded data_quality_labels.csv file.

The datestamp corresponds to the year, month and day the file was shared.

# How To Use Data Quality Labels to Filter Data

The first row of the `data_quality_thresholds.csv` file includes the labels used to describe each category of data quality. At the time of writing this document, those labels are `committed, active, intermittent, limited-surveys, limited-sensors, few-sensors`. These labels are applied to each writer ID in the `data_quality_labels.csv` file. In order to select data that meet the thresholds for a given label, you can match Search results on writer ID.

An example script has been provided in this repository called `downselect_example.py`. This example will show how to filter query results based on desired data quality labels. The script makes a search query, then filters for data that has been labeled either `active` or `committed`. The script can be run by passing the filepath to the data quality labels csv as an argument.
```bash
./downselect_example.py <datestamp>_data_quality_labels.csv
```
The expected output is a list of record_ids.
