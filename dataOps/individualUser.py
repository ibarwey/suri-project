import pymongo
import json
import time
import datetime
import sys
import numpy

#url = 'mongodb://localhost:27017/'
url = 'mongodb://localhost:27014/'

dbase = sys.argv[1]
print("database: " + str(dbase))

client = pymongo.MongoClient(url)
db = client[dbase]
usersCol = db['users']
responsesCol = db['responses']
percentArray = []
dataArray = []
fnrArray = []
#specify ground truth for each question
groundtruth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 2,2,2,2, 1,1,1, 2, 3, 5] #40 none, 5 knife, 3 gun, 1 wrench, 1 scissor

for user in usersCol.find():

    userName = user['user']
    userResponse = responsesCol.find({"user":userName})
    #print(userResponse["q1"])
    print(userName)
    demographic = user["surveyResults"]
    fnr = 0
    score = user['score']
    if(score != "None"):
        print(score)
        percentArray.append(score*100/50)

    for x in userResponse:
        if(x["question"] > 15 and x["q1"] != 1):
            fnr = fnr+1

    print(fnr)
    if(fnr>25):
        fnrArray.append(100)
    else:
        fnrArray.append((fnr*100/25))

    print("FNR = ",(fnr*100/25))
print(percentArray)
print(fnrArray)

#average percentage
sum = 0
for i in range(len(percentArray)):
    sum = sum + percentArray[i]

avg = sum/len(percentArray)
array = numpy.array(percentArray)
print("Min : " + str(numpy.min(array)))
print("Max : " + str(numpy.max(array)))
print("Average Score %" + str(avg))

#average fnr percentage
sum = 0
for i in range(len(fnrArray)):
    if(fnrArray[i] > 100):
        sum = sum+100
    else:
        sum = sum + fnrArray[i]

avg = sum/len(fnrArray)
array = numpy.array(fnrArray)
print("Min : " + str(numpy.min(array)))
print("Max : " + str(numpy.max(array)))
print("Average FNR  %" + str(avg))
