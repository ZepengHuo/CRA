import os
import json 
import matplotlib.pyplot as plt
import pandas as pd

# good bad agnostic
frequencySensorMap = {}

# Good Actors
path = ('/data/datasets/CRA/good_actors_Mar6_2022')
print('='*20, 'good', '='*20)
for root, dirs, files in os.walk(path, topdown=False):
   print(root)
   for filename in files:
      if filename[-4:] == 'json':
        #Read json contents
        try:
          f = open("".join([root,"/",filename]),"r")
          data = json.load(f)
        except:
          print("An error occured while opening the file")
          break
        
        #Grabbing Sensor type and adding it into distribution
        sensorName = data['type'].replace("kry-sensor-","")
        if sensorName not in frequencySensorMap:
            frequencySensorMap[sensorName] = 0
        frequencySensorMap[sensorName] += 1
        
        f.close()

# Bad Actors
path = ('/data/datasets/CRA/bad_actors_Mar6_2022')
print('='*20, 'bad', '='*20)
for root, dirs, files in os.walk(path, topdown=False):
  print(root)
  for filename in files:
    if filename[-4:] == 'json':
      #Read json contents
      try:
        f = open("".join([root,"/",filename]),"r")
        data = json.load(f)
      except:
        print("An error occured while opening the file")
      
      #Grabbing Sensor type and adding it into distribution
      sensorName = data['type'].replace("kry-sensor-","")
      if sensorName not in frequencySensorMap:
          frequencySensorMap[sensorName] = 0
      frequencySensorMap[sensorName] += 1
      f.close()

print(frequencySensorMap)

df = pd.DataFrame({'Type':list(frequencySensorMap.keys()),'Freq':list(frequencySensorMap.values())})
df_sorted = df.sort_values('Freq',ascending = True)
df_sorted.to_csv(path[-9:]+'.csv')


plt.figure(figsize=(15,15))
plt.barh('Type','Freq', data = df_sorted)
plt.xlabel("Frequency of Sensors")
plt.ylabel("Sensors")
plt.show()
plt.savefig("frequency_map.png", dpi=150)
print(list(frequencySensorMap.keys()))