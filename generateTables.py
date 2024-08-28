import pandas as pd
import numpy as np
import itertools
import os

path = 'Data2/MELODY_2.csv'

df = pd.read_csv(path, sep='\t', index_col=[0])

pitchdf = pd.DataFrame(columns=['pitch', 'count', 'next_pitch', 'count_next_pitch', 'probability_next_pitch'])

pitchdf['pitch'] = df['pitch']

countlist = []
for i in pitchdf['pitch']:
    counter = 0
    for j in pitchdf['pitch']:
        if(i == j):
            counter += 1
    countlist.append(counter)
countlist_s = pd.Series(countlist)
pitchdf['count'] = countlist_s

pitchdf['next_pitch'] = pitchdf['pitch'].shift(periods=-1)

pitchToList = pitchdf['pitch'].tolist()
nextPitchToList = pitchdf['next_pitch'].tolist()

nextPitchList = list(zip(pitchToList, nextPitchToList))
countlist2 = []

for q in nextPitchList:
    counter = 0
    for r in nextPitchList:
        if q == r:
            counter += 1
    countlist2.append(counter)

countlist2_s = pd.Series(countlist2)

pitchdf['count_next_pitch'] = countlist2_s
pitchdf['probability_next_pitch'] = pitchdf['count_next_pitch'] / pitchdf['count']
pitchdf['probability_next_pitch'] = pitchdf['probability_next_pitch'].round(2)

pitchdf.to_csv("Tables/Pitch_Table.csv", sep='\t')
print(pitchdf)