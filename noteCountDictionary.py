import pickle
import pandas as pd

df = pd.read_csv("Tables/Pitch_Table.csv", sep='\t', index_col=[0])

pitchToList = df['pitch'].tolist()
pitchKeys = list(dict.fromkeys(pitchToList))

pitchCountToList = df['count'].tolist()
pitch_counts = dict(zip(pitchToList, pitchCountToList))

df['next_pitch'] = df['next_pitch'].fillna(0)
nextToList = df['next_pitch'].tolist()
df['count_next_pitch'] = df['count_next_pitch']
countNextToList = df['count_next_pitch'].tolist()
countList = df['count'].tolist()

comparePitch = dict(zip(pitchToList, nextToList))
pitch_counts = dict(zip(pitchToList, countList))
pitch_transitions = {}

counter = 0
for i in pitchToList:
    pitch_transitions[i] = {}

for j in pitchToList:
    for k in pitchToList:
        df2 = df.loc[(df['pitch'] == j) & (df['next_pitch'] == float(k))]
        df2 = df2.set_index('pitch')
        if df2.empty:
            pitch_transitions[j][k] = 0
        else:
            l = df2['count_next_pitch'].tolist()
            pitch_transitions[j][k] = l[0]

with open('note_counts.txt', 'wb') as w:
    w.write(pickle.dumps(pitch_counts))
w.close()
with open('p_next_note_counts.txt', 'wb') as file:
    file.write(pickle.dumps(pitch_transitions))
file.close()


