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
groundtruth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ,1,1,1,1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4,4,4,4, 5,5, 6] #25 none, 7 gun, 4 knife, 4 wrench, 7 pliers, 2 scissors, 1 hammer

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
        percentArray.append(score*100/30)

    for x in userResponse:
        if(x["question"] > 15 and x["q1"] != 1):
            fnr = fnr+1

    print(fnr)
    if(fnr>15):
        fnrArray.append(100)
    else:
        fnrArray.append((fnr*100/15))

    print("FNR = ",(fnr*100/15))
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
