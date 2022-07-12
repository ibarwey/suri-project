import pymongo
import json
import time
import datetime
import sys

#url = 'mongodb://localhost:27017/'
url = 'mongodb://localhost:27014/'

dbase = sys.argv[1]
print("database: " + str(dbase))

client = pymongo.MongoClient(url)
db = client[dbase]
usersCol = db['users']
responsesCol = db['responses']

dataArray = []

for user in usersCol.find():

    userResponse = {}

    userName = user['user']
    print(userName)

    userResponse["name"] = userName

    for i in range(1,51):
        print(i," = LOOP ENTERED")
        response = responsesCol.find_one({"user": userName, "question": i})
        userResponse[i] = {
            "time": response["time"],
            "q1": response["q1"],
            "boundingBox": response["boundingBox"],
            "mouseArray": response["mouseArray"]
        }

    dataArray.append(userResponse)

rightNow = datetime.datetime.today().strftime('%m-%d-%Y')
file_name = rightNow + dbase + ".json"

with open(str(file_name), 'w+') as outfile:
	json.dump(dataArray, outfile)
