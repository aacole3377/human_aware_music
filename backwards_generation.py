import numpy as np
import pandas as pd
import random
from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct
import pickle
import miditapyr as mt
import mido

def reverseList(lst):
    l = []
    for i in reversed(lst):
        l.append(i)
    return l

def toMidi(df):
    # create an empty file
    mido_obj = mid_parser.MidiFile()
    beat_resol = mido_obj.ticks_per_beat

    # create an  instrument
    track = ct.Instrument(program=0, is_drum=False, name='Melody')
    mido_obj.instruments = [track]

    for index, row in df.iterrows():
        start = row['start']
        end = row['end']
        pitch = row['pitch']
        velocity = row['velocity']
        note = ct.Note(start=start, end=end, pitch=pitch, velocity=velocity)
        mido_obj.instruments[0].notes.append(note)

        # prepare next
        # prev_end = end
        # pitch += 1

    # create markers
    marker_hi = ct.Marker(time=0, text='HI')
    mido_obj.markers.append(marker_hi)

    # write to file
    mido_obj.dump('MidiDumps/9.midi')

    # reload for check
    # mido_obj_re = mid_parser.MidiFile('Melody_1.midi')
    # for note in mido_obj_re.instruments[0].notes:
    #     print(note)


path = "Tables/9.csv"

df = pd.read_csv(path, sep="\t", index_col=[0])

pitchList = df['pitch'].tolist()
df['next_pitch'] = df['next_pitch'].fillna(0)
nextPitchList = df['next_pitch'].tolist()
countList = df['count'].tolist()

pitchCounts = dict(zip(pitchList, countList))

# pitchList = reverseList(pitchList)
# nextPitchList = reverseList(nextPitchList)
# countList = reverseList(countList)

pitch_transitions = {}

for i in pitchList:
    pitch_transitions[i] = {}

for j in pitchList:
    for k in pitchList:
        selector = (df['pitch'] == j) & (df['next_pitch'] == float(k))
        if np.sum(selector) == 0:
            pitch_transitions[j][k] = 0
        else:
            pitch_transitions[j][k] = df.loc[selector].iloc[0]['count_next_pitch']

newPitch = []
current_note = pitchList[len(pitchList) - 1]
current_note = pitchList[0]
note_count = 0


while note_count < 264:
    selector = random.randint(0, pitchCounts[current_note])
    for next_note in pitch_transitions[current_note]:
        selector -= pitch_transitions[current_note][next_note]
        if selector <= 0:
            current_note = next_note
            break
    newPitch.append(int(current_note))
    note_count += 1

newPitch_s = pd.Series(newPitch)
df['pitch'] = newPitch_s

newSong = pd.DataFrame(columns=['start', 'end', 'pitch', 'velocity'])

newSong['start'] = df['start']
newSong['end'] = df['end']
newSong['pitch'] = df['pitch']
newSong['velocity'] = df['velocity']
newSong.dropna(subset=['start'], inplace=True)
newSong['start'] = newSong['start'].astype(int)
newSong['end'] = newSong['end'].astype(int)
# newSong['pitch'] = newSong['pitch'].astype(int)
newSong['velocity'] = newSong['velocity'].astype(int)

print(newSong.head())

newSong.to_csv("MidiDumps/0data.csv", sep="\t")

toMidi(newSong)

# with open('reversed_notes.txt', 'wb') as file:
#     file.write(pickle.dumps(pitch_transitions))
# file.close()