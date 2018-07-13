#How to use: python ConvertToCsv.py 'path_to_channel_to_convert' 'path_to_slack_users_json.csv' 'output_file.csv'
#Example: python ConvertToCsv.py export/Channel1 export/users.json output.csv

import sys, json, os, csv
from datetime import datetime


jsonPath = sys.argv[1]
jsonUsers = sys.argv[2]
outcsv = sys.argv[3]

channel_list = [] #list of public channels
userList = [] #list of users taken directly from json file
user = {} #dictionary of a single user

#choosing what user data to store
with open(jsonUsers) as userData:
	userList = json.load(userData)
	for data in userList:
		userID = data["id"] #unique id given to each user by slack
		name = data["name"] #here we are getting the username of each slack meber and not their actual name
		user[userid] = [name]

with open(outcsv) as out:
	writer = csv.writer(out,delimiter=',',newline='\n')
	for channel in os.listdir(jsonPath): #for every channel
		channel_list.append(channel)
		with open(jsonPath + '/' + channel) as data_file:
			data = json.load(data_file)
			for item in data:
				if item["type"] == "message": #TO DO: Look into other possilbe types, see what we can extract
					#Here is where we will choose what exact data to extract from the messages
					userFrom = user[item["user"]]
					#timestamp
					ts = datetime.utcfromtimestamp(float(item['ts']))
					time = ts.strftime("%Y-%m-%d %H:%M:%S")
					writer.writerow([time.encode('utf-8'),userFrom.encode('utf-8')])