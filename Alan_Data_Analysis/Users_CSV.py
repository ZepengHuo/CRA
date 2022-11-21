from email.mime import audio
import os
import json
import sndhdr
from socketserver import DatagramRequestHandler 
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

MonthDate = 'Mar6_2022'
userGoodness = 'good'

questionMap = {} 
#sensorList = ['a-gyroscope']
frequencyMap_df = pd.read_csv(MonthDate+'.csv')
sensorList = frequencyMap_df['Type'].tolist()

sensorType = ''
myList = []
# Renames the columns from the super_dict
def renamedKey(sensorType):
  #Gather the keys and rename them in a list
  name_of_header = sensorType.replace("-kry-sensor","")
  #sensorKey = name_of_header + "-" + sensorKey
  #return sensorKey
  return name_of_header

def exportUserData(super_dict,csv_filename):
  df = pd.DataFrame.from_dict(super_dict, orient='index')
  df1 = df.T
  # col_lst = [] 
  # for col_name in column_name_lst:
  #   if "timestamp" in col_name:
  #     continue
    # col_lst.append(col_name)
  # df.dropna(subset = ['i-magnetometer-y', 'i-magnetometer-z', 'i-magnetometer-x'], how = 'all')
  # df2 = df1.fillna(0)
  # df2.replace(0,"N/A",inplace=True)
  # #Move timestamp column to the right
  # cols_at_end = ['i-magnetometer-timestamp']
  # df2 = df2[[c for c in df2 if c not in cols_at_end] 
  #         + [c for c in cols_at_end if c in df2]]
  df1.to_csv('/data/datasets/CRA/Exported_User_Data_CSVs_/'+csv_filename+'.csv')
  print(df1)

# Good/bad Actors Dataset
path = ('/data/datasets/CRA/'+userGoodness+'_actors_' + MonthDate)
for root, dirs, files in os.walk(path, topdown=False):
  index = root.rfind("/")
  csv_filename = root[index+1:]#Directory is user csv name
  super_dict = {}
  df = pd.DataFrame()
  for filename in files:
    if filename[-4:] == 'json':
      
      
      # 1）Read json-metadata contents
      try:
        f = open("".join([root,"/",filename]),"r")
        data = json.load(f)
        sensorType = data['type'].replace("-kry-sensor","")
        if sensorType not in  sensorList:
          continue
      except ValueError:
        print("An error occured while opening the file " + filename)
        continue
      f.close() #closing the metadata file. Opening the raw data below
      
      
      # 2） Path to the raw data file
      raw_path = "".join([root,"/",filename[:-14]])
      f = open(raw_path,"r")
      data = json.load(f)
      f.close() #close raw fata file
      
      #Issue1: code may append data to the incorect timestamp
      #Issue3: code sometimes may skip over some keys as it only recognizes the keys from the first row of data (time,x,y,z) may miss columns(time,x,y,z,x2,y2)
      #Conisder: All rows of the data must be in the correct order according to the timestamp
      #(Might be buggy)This code block merges all dictionary info in a raw data file and merges t into a single dictionary with keys(x,y,z) and their values

      for dict in data['records']:
        for key in dict:
          renamed_Key = renamedKey(key)
          if renamed_Key not in df.columns:
            #New column header to add to the df. 
            #df[renamed_Key] = ""
            df.insert(0, renamed_Key, dict[key])  
            #Insert at correct row and column
          else:
            #Add this data to the corresponding column in the df. Would this insert in the correct order?
            df[renamed_Key] = dict[key]
            
          #if key not in dict. Add a new column to the df
          #else add the key value to the correponding column cell
  print(df)
  exportUserData(super_dict,csv_filename)
        


# #Path to the single file I am working with 
# path ='/data/datasets/CRA/good_actors_Mar6_2022/c75c240a-788a-4e27-9332-67b88e0132fe/71053e32-21c7-40ed-b8b5-46c1c6e73de0'
# f = open(path,"r")
# data = json.load(f)


# #This code block gathers all the information in a raw data file and merges it into a single dictionary with keys(x,y,z) and their values s a list
# for d in data['i-kry-sensor-magnetometer']:
#     for k, v in d.items():
#         if super_dict.get(k) is None:
#             super_dict[k] = []
#         if v not in super_dict.get(k):
#             super_dict[k].append(v)

# #This code block just gathers and renames the different keys (x,y,z,timestamp) contained in a raw data file
# for datum in data['i-kry-sensor-magnetometer']: 
#   column_name_lst = list(datum.keys())
#   break
# #Gather the keys and rename them in a list
# name_of_header = 'i-kry-sensor-magnetometer'.replace("-kry-sensor","")
# for i in range(len(column_name_lst)):
#   column_name_lst[i] = name_of_header + "-" + column_name_lst[i]
# indx = 0
# #Rename the keys to something more useful
# for key in list(super_dict.keys()):
#   super_dict[column_name_lst[indx]] = super_dict.pop(key)
#   indx+=1


# df = pd.DataFrame.from_dict(super_dict, orient='index')
# df1 = df.T
# col_lst = [] 
# for col_name in column_name_lst:
#   if "timestamp" in col_name:
#     continue
#   col_lst.append(col_name)
# # df.dropna(subset = ['i-magnetometer-y', 'i-magnetometer-z', 'i-magnetometer-x'], how = 'all')
# df2 = df1.fillna(0)
# df2.replace(0,"N/A",inplace=True)
# # #Move timestamp column to the right
# # cols_at_end = ['i-magnetometer-timestamp']
# # df2 = df2[[c for c in df2 if c not in cols_at_end] 
# #         + [c for c in cols_at_end if c in df2]]
# df2.to_csv('testing.csv')