import numpy as np
import pandas as pd
import random
import pickle

df = pd.read_csv("Data2/MELODY_15.csv", sep="\t", index_col=[0])
pitchdf = pd.read_csv("Tables/Pitch_Table.csv", sep="\t", index_col=[0])

def valueCount(listToCount):
    countList = []
    for i in listToCount:
        count = 0
        for j in listToCount:
            if i == j:
                count += 1
        countList.append(count)
    return countList

# need duration values, followed by rest value, followed by count
# then we can generate start and end values

durationToList = pitchdf['duration'].tolist()
restValToList = pitchdf['rest_duration'].tolist()
durr_rest = list(zip(durationToList, restValToList))
durationCountList = valueCount(durationToList)
durr_count = dict(zip(durationToList, durationCountList))
durr_rest_count = valueCount(durr_rest)

duration_rest_counts = {}

for i in durationToList:
    duration_rest_counts[i] = {}

for j in durationToList:
    for k in restValToList:
        selector = (pitchdf['duration'] == j) & (pitchdf['rest_duration'] == float(k))
        if np.sum(selector) == 0:
            duration_rest_counts[j][k] = 0
        else:
            duration_rest_counts[j][k] = pitchdf.loc[selector].iloc[0]['rest_count']

current_note = 62
start = 0
end = 40
startList = []
endList = []
endList.append(end)
startList.append(start)
note_count = 0

while note_count < 264:
    selector = random.randint(0, durr_count[current_note])
    for next_note in duration_rest_counts[current_note]:
        selector -= duration_rest_counts[current_note][next_note]
        if selector <= 0:
            current_note = next_note
            start += random.choice(list(durationToList)) + next_note
            end = start + 300
            print("Start: ", start)
            print("End: ", end)
            break
    startList.append(int(start))
    endList.append(int(end))
    note_count += 1


dfsong = pd.DataFrame(columns=['start', 'end', 'pitch', 'velocity'])
startList_s = pd.Series(startList)
endList_s = pd.Series(endList)
dfsong['start'] = startList_s
dfsong['end'] = endList_s
dfsong['velocity'] = 108



dfsong.to_csv("Tables/song.csv", sep='\t')
