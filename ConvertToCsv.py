#How to use: python ConvertToCsv.py 'path_to_channel_to_convert' 'path_to_slack_users_json.csv' 'output_file.csv'
#Example: python ConvertToCsv.py export/Channel1 export/users.json output.csv

import sys, json, os, csv
from datetime import datetime


jsonPath = sys.argv[1]
#print(os.listdir(jsonPath))
jsonUsers = sys.argv[2]
outcsv = sys.argv[3]

channel_list = [] #list of public channels
userList = [] #list of users taken directly from json file
user = {} #dictionary of a single user
userByName = {} #used to get user ID from the Name of the User
#list of message subtypes to be ignored
ignoreList = ['channel_join','channel_leave','channel_topic','channel_purpose','channel_name','channel_archive'
	,'Channel_unarchive','group_join','group_leave','group_topic', 'group_purpose','group_name','group_archive'
	,'group_unarchive','pinned_item','unpinned_item']

#choosing what user data to store
with open(jsonUsers) as userData:
	userList = json.load(userData)
	for data in userList:
		userID = data["id"] #unique id given to each user by slack
		name = data["name"] #here we are getting the username of each slack meber and not their actual name
		user[userID] = [name]
		userByName[name] = [userID]

#print(user)

with open(outcsv, 'w') as out:
	writer = csv.writer(out,delimiter=',')
	writer.writerow(['Time_Stamp','Year','Month','Day','Time','User_Name','User_ID','Reacted_By'])
	for channel in os.listdir(jsonPath): #for every channel
		print(channel)
		channel_list.append(channel)
		with open(jsonPath + '/' + channel) as data_file:
			data = json.load(data_file, encoding = "latin-1")
			for item in data:
				try:
					if item["subtype"] in ignoreList:
						continue #skip message
				except:
					pass

				if item["type"] == "message": #Here is where we will choose what exact data to extract from the messages
					#remove hidden or deleted messages
					try:
						if item["hidden"] == True and item["subtype"] == "message_deleted":
							continue #skip message
					except:
						pass

					#get the user that sent the messge
					try:
						userFrom = user[item["user"]]
						print(userFrom)
					except:
						#if "user" is not present, then the message must have been edited,
						#in which case we'll need to look for it in "message"
						try:
							userFrom = user[item["message"]["user"]]
							print(userFrom)
						except:
							print("No User info found for this message")
							continue #skip message
					
					#get the time info of the messge
					ts = datetime.utcfromtimestamp(float(item['ts']))
					time = ts.strftime("%H:%M:%S")
					year = ts.year
					month = ts.month
					day = ts.day

					#get reactions info
					reactions = [] #list of users that reacted to a message
					tempList = []
					try:
						reactlist = item["reactions"]
						for reaction in reactlist: #for every reaction
							for reactUser in reaction['users']: #for every user
								tempList.extend(userByName[reactUser])
							reactions.extend(tempList)
					except Exception:
						pass	

					try:
						writer.writerow([item['ts'],year,month,day,time,userFrom,item["user"],reactions])
					except:
						writer.writerow([item['ts'],year,month,day,time,userFrom,item["message"]["user"],reactions])
					#To Do: Check if we need to remove User has joined the channel