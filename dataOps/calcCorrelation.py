import json
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
from scipy.stats.stats import pearsonr
import seaborn as sns

with open('12-02-2020Test2-1.json') as f:
    data = json.load(f)

#specify ground truth for each question
groundtruth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ,1,1,1,1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4,4,4,4, 5,5, 6] #25 none, 7 gun, 4 knife, 4 wrench, 7 pliers, 2 scissors, 1 hammer

times = []
correctAnswer = []

for i in range(1,31):

    for userResponse in data:
        response = userResponse[str(i)]
        times.append(response["time"])
        userAnswer = response["q1"]

        correct = None
        #check if correct
        if userAnswer == groundtruth[i-1]:
            correct = 1
        else:
            correct = 0

        correctAnswer.append(correct)

corr, _ = pearsonr(times, correctAnswer)
print(corr)

#calculate correlation
plt.scatter(times, correctAnswer)

sns.regplot(x=times, y=correctAnswer, data=data, logistic=True)

#plt.clf()
plt.xlabel("Time (seconds)")
plt.ylabel("Correct/Incorrect")
plt.ylim(-.25, 1.25)
plt.xlim(0, 70)
plt.show()
