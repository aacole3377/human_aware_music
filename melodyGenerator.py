import pickle
import random

import pandas as pd
from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct

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
    mido_obj.dump('MidiDumps/Generated_Pitch.midi')

    # reload for check
    # mido_obj_re = mid_parser.MidiFile('Melody_1.midi')
    # for note in mido_obj_re.instruments[0].notes:
    #     print(note)

with open("note_counts.txt", "rb") as f:
    data = pickle.load(f)
with open("p_next_note_counts.txt", "rb") as g:
    nextData = pickle.load(g)

pitch_counts = data
pitch_transitions = nextData
current_note = 75
pitchList = []
note_count = 0

while note_count < 264:
    selector = random.randint(0, pitch_counts[current_note])
    for next_note in pitch_transitions[current_note]:
        selector -= pitch_transitions[current_note][next_note]
        if selector <= 0 and (pitch_transitions[current_note][next_note] / pitch_counts[current_note]) < 0.50:
            current_note = next_note
            break
    pitchList.append(current_note)
    note_count += 1

print("Pitch list size: ", len(pitchList))
print(pitchList)
pitchList_s = pd.Series(pitchList)

path = "Data2/MELODY_15.csv"

tempdf = pd.read_csv(path, sep="\t", index_col=[0])

colstokeep = ['start', 'end', 'pitch', 'velocity']
newSong = tempdf[colstokeep]
newSong['pitch'] = pitchList_s
print(newSong)
toMidi(newSong)

