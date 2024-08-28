import miditoolkit
import pandas as pd
import mido
import numpy as np
from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct
import os

path0 = 'Data2/MELODY_1.csv'
path1 = 'Data2/MELODY_3.csv'
path2 = 'Data2/MELODY_4.csv'
path3 = 'Data2/MELODY_5.csv'

dfList = []

df0 = pd.read_csv(path0, sep='\t', index_col=[0])
df1 = pd.read_csv(path1, sep='\t', index_col=[0])
df2 = pd.read_csv(path2, sep='\t', index_col=[0])
df3 = pd.read_csv(path3, sep='\t', index_col=[0])

dfList.append(df0)
dfList.append(df1)
dfList.append(df2)
dfList.append(df3)

print("DF0---------\n", df0['pitch'])
print("DF3---------\n", df3['pitch'])

df0['pitch'] = df3['pitch']
# df0['start'] = df3['start']
# df0['end'] = df3['end']

# create an empty file
mido_obj = mid_parser.MidiFile()
beat_resol = mido_obj.ticks_per_beat

# create an  instrument
track = ct.Instrument(program=0, is_drum=False, name='Melody')
mido_obj.instruments = [track]

for index, row in df0.iterrows():
    start = row['start']
    end = row['end']
    pitch = row['pitch']
    velocity = row['velocity']
    note = ct.Note(start=start, end=end, pitch=pitch, velocity=velocity)
    mido_obj.instruments[0].notes.append(note)

    # prepare next
    # prev_end = end
    # pitch += 1

# print(df0['beat_Duration'].round(2))

# create markers
marker_hi = ct.Marker(time=0, text='HI')
mido_obj.markers.append(marker_hi)

# write to file
mido_obj.dump('Melody_1.midi')

# reload for check
mido_obj_re = mid_parser.MidiFile('Melody_1.midi')
for note in mido_obj_re.instruments[0].notes:
    print(note)

print('\nmarker:', mido_obj_re.markers)

