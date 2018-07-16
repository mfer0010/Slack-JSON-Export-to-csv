#How to use: python ConvertToCsv.py 'path_to_channel_to_convert' 'path_to_slack_users_json.csv' 'output_file.csv'
#Example: python ConvertToCsv.py export/Channel1 export/users.json output.csv

import sys, json, os, csv
from datetime import datetime


jsonPath = sys.argv[1]
print(os.listdir(jsonPath))
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
		user[userID] = [name]


with open(outcsv, 'w') as out:
	writer = csv.writer(out,delimiter=',')
	writer.writerow(['Time Stamp','Date/Time','User Name'])
	for channel in os.listdir(jsonPath): #for every channel
		print(channel)
		channel_list.append(channel)
		with open(jsonPath + '/' + channel) as data_file:
			data = json.load(data_file, encoding = "latin-1")
			for item in data:
				if item["type"] == "message":
					#Here is where we will choose what exact data to extract from the messages
					userFrom = user[item["user"]]
					#timestamp
					ts = datetime.utcfromtimestamp(float(item['ts']))
					date = ts.strftime("%Y-%m-%d %H:%M:%S")
					writer.writerow([item['ts'],date,userFrom])
#					#To add: If reactions have been made, save info on reactions
					#To Remove: User whatever has joined a chat