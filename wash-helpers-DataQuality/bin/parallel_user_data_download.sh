#!/bin/bash
# Script to download all records for a list of users in multiple files
# where each file of users is downloaded in parallel

# Update this array to include a number string for each file of user ids to download
# or remove number strings if using less files
# e.g. if using 11 files, add '11', if using 2 files of user ids, delete the number strings 3-10
AR=('1' '2' '3', '4' '5' '6', '7', '8', '9', '10')
for i in "${!AR[@]}"; do
	echo "Starting download of user data for users listed in: part_$(expr $i + 1)_user_ids_to_download.txt, sending output to part_$(expr $i + 1)_user_ids_to_download.out"
	# Run download of records for user ids in the background, creating an output file for this specific download process
	nohup python3 wash-helper.py user-data -f part_$(expr $i + 1)_user_ids_to_download.txt > part_$(expr $i + 1)_user_ids_to_download.out 2>&1&
done

echo "Run ps -eaf | grep [wash]-helper.py | awk '{print $2}' | xargs kill -9 on a unix shell to terminate all background processes started by this script."
echo "Downloads running in the background, check the .out files to monitor progress."
echo "NOTE: Any records that have previously been downloaded and are listed in the record_id_file.txt will not be redownloaded. To force a re-download run rm record_id_file.txt from the command line or delete that file using the filesytem UI for your platform."
echo "Run  rm -rf ./downloads *.out download_error_record_ids_file.txt to cleanup all logs and downloaded files."
