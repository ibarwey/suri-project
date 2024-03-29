#
# Aggregation Models Test
#
# Author: Ryan Kemmer, Yeawon Yoo
#
# v3__ updated on Dec 7 09:04


import json
import math

def tieCheck(x):
    if x.count(x[0]) == len(x):
        return True
    else:
        return False

def checkAnswer(x,gtruth):
    if x == -1: #if x is a tie, change the value to be incorrect
        if gtruth == 0:
            x = 1
        else:
            x = 0
    if gtruth == 0 and x == 0:
        return 'TN'
    elif gtruth == 0 and x != 0:
        return 'FP'
    elif gtruth != 0 and x == 0:
        return 'FN'
    else:
        return 'TP'

def countAnswer(array):
    tnCount = 0
    fnCount = 0
    fpCount = 0
    tpCount = 0
    for i in range(len(array)):
        if(array[i] == 'TN'):
            tnCount+=1;
        elif(array[i] == 'FN'):
            fnCount+=1;
        elif(array[i] == 'FP'):
            fpCount+=1;
        else:
            tpCount+=1;

    print("True Postives Count: " + str(tpCount));
    print("False Positives Count: " + str(fpCount));
    print("True Negatives Count: " + str(tnCount));
    print("False Negatives Count: " + str(fnCount));



def majorityVote(predictions):

    #specify binary decisions(1 for yes and 0 for no)
    choices = [0,1,2,3,4,5,6]
    #list to count majority votes
    choiceCounts = [0] * len(choices)

    #count each vote
    for i in range(len(choices)):
        for p in predictions:
            if p == choices[i]:
                choiceCounts[i] +=1

    print("vote outcome:", choiceCounts)

    #check to see if there is a tie
    tie = tieCheck(choiceCounts)
    #return winner (0 for No, 1 for yes, -1 for tie)
    if tie == False:
        ind = choiceCounts.index(max(choiceCounts))
        if ind == 0:
            winner = 1
        elif ind == 1:
            winner = 0
    else:
        winner = -1

    return winner

def honeypot(predictions, trap):

    #specify binary decisions(1 for yes and 0 for no)
    choices = [1,0]

    #list to count majority votes
    choiceCounts = [0] * len(choices)

    #count each vote to q1
    for i in range(len(choices)):
        for j in range(len(predictions)):
            # if judge j returns correct answers to all the trapping questions
            if (predictions[j] == choices[i]) and (trap[j] == max(trap)):
                choiceCounts[i] += 1

    #print(choiceCounts)

    #check to see if there is a tie
    tie = tieCheck(choiceCounts)
    #return winner (0 for No, 1 for yes, -1 for tie)
    if tie == False:
        ind = choiceCounts.index(max(choiceCounts))
        if ind == 0:
            winner = 1
        elif ind == 1:
            winner = 0
    else:
        winner = -1
    return winner

def weighted_honeypot(predictions, trap):

    #specify binary decisions(1 for yes and 0 for no)
    choices = [1,0]

    #list to count majority votes
    choiceCounts = [0] * len(choices)
    #count each vote to q1
    for i in range(len(choices)):
        for j in range(len(predictions)):
            # if judge j returns correct answers to all the trapping questions
            if predictions[j] == choices[i]:
                choiceCounts[i] += 1*trap[j]/(max(trap)*1.0)

    #print(choiceCounts)

    #check to see if there is a tie
    tie = tieCheck(choiceCounts)
    #return winner (0 for No, 1 for yes, -1 for tie)
    if tie == False:
        ind = choiceCounts.index(max(choiceCounts))
        if ind == 0:
            winner = 1
        elif ind == 1:
            winner = 0
    else:
        winner = -1
    return winner



def ELICE(predictions, groundtruth, trap_true, trap_false):

    #alpha = expertise level --> reliability of judge
    alpha = [0] * len(predictions)
    #beta = difficulty of questions
    beta = 0
    P = 0


    for i in range(len(predictions)):
        alpha[i] += (trap_true[i] - trap_false[i])*1/3.0
        if predictions[j] == groundtruth:
            beta += 1/(len(predictions)*1.0)

    #score --- inferred labels
    for i in range(len(predictions)):
        if predictions[i] == 1:
            P += (1/(len(predictions)*1.0))*(1/(1+math.exp(-alpha[i]*beta)))*predictions[i]
        else:
            P += (1/(len(predictions)*1.0))*(1/(1+math.exp(-alpha[i]*beta)))*(-1)

    #return winner (negative for No, positive for yes,)
    if P >= 0:
        winner = 1
    else:
        winner = 0
    return winner

#main
#

#load json file
with open('08-05-2021Test4_3_1.json') as f:
    data = json.load(f)

#specify ground truth for each question
groundtruth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 2,2,2,2, 1,1,1, 2, 3, 5] #40 none, 5 knife, 3 gun, 1 wrench, 1 scissor
#honeypots (indexed starting at 0)
honeypots = [2,3,14,15]

trap_true = [0]*48
trap_false = [0]*48

#fill values in trap_true and trap_false arrays
for i in range(50):

    predictions = []

    for userResponse in data:
        response = userResponse[str(i + 1)]
        predictions.append(response["q1"])

    if i in honeypots:
        for j in range(len(predictions)):
            if predictions[j] == groundtruth[i]:
                trap_true[j] +=1
            else:
                trap_false[j] +=1


#aggregation method totals
majTotals = []
hpTotals = []
whTotals = []
eTotals = []

#calculate results
for i in range(50):

    predictions = []

    for userResponse in data:
        response = userResponse[str(i + 1)]
        predictions.append(response["q1"])

    print('************ Question: ' + str(i+1) + ' ===> Ground Truth: ' + str(groundtruth[i]) + '**************')
#    print('==================================')
    print('Majority Winner: ' + str(majorityVote(predictions)))
#    print('==================================')

    if i not in honeypots:

        print('Honeypot Winner: ' + str(honeypot(predictions, trap_true)))
        print('Weighted Honeypot Winner: ' + str(weighted_honeypot(predictions, trap_true)))
        print('ELICE: ' + str(ELICE(predictions, groundtruth[i], trap_true, trap_false)))

        #add to array of predictions
        majTotals.append(checkAnswer(majorityVote(predictions),groundtruth[i]))
        hpTotals.append(checkAnswer(honeypot(predictions, trap_true),groundtruth[i]))
        whTotals.append(checkAnswer(weighted_honeypot(predictions, trap_true),groundtruth[i]))
        eTotals.append(checkAnswer(ELICE(predictions, groundtruth[i], trap_true, trap_false),groundtruth[i]))

print(str("---------------------- Totals ------------------------"))

print("Majority Totals: ")
countAnswer(majTotals)

print("Honey Pot Voting Totals")
countAnswer(hpTotals)

print("Weighted Honey Pot Voting Totals")
countAnswer(whTotals)

print("ELICE Voting Totals")
countAnswer(eTotals)

'''
print('Majority Vote Totals: ' + sum())

print('Honeypot Winner: ' + )

print('Weighted Honeypot Winner: ' + )

print('ELICE: ' + )
'''
