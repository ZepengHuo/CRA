#!/bin/bash

label_quality_csv='./wash-helpers-DataQuality/20211012_data_quality_labels.csv'
save_location='./wash-helpers-0.2/downloads/new_context_QualifiedUsers'
top_users=3
phone_type='iPhone' 


python wash-helpers-0.2/get_SurveyDatum_onActivity.py  $label_quality_csv  $save_location  $top_users  $phone_type
