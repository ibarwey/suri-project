import json
import matplotlib.pyplot as plt
import seaborn as sns

#load json file
with open('12-02-2020Test2-1.json') as f:
    data = json.load(f)

groundtruth = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ,1,1,1,1,1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4,4,4,4, 5,5, 6] #25 none, 7 gun, 4 knife, 4 wrench, 7 pliers, 2 scissors, 1 hammer

correctDist = []

#iterate through users
for i in range(len(data)):
    correct = 0
    for j in range(1,31):
        response = data[i][str(j)]
        useRes = response["q1"]
        if useRes == groundtruth[j-1]:
            correct += 1

    correctDist.append(correct)

correctDist.sort()
print(correctDist)

x_pos = x_pos = [i for i, _ in enumerate(correctDist, 1)]
scatter = sns.scatterplot(x = x_pos, y = correctDist)
plt.ylabel('Number Correct')
plt.xlabel('User ID')
plt.show()
