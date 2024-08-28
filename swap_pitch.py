import pandas as pd
import numpy as np
from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct

class FindPattern:
    def __init__(self, dframe):
        self.patternList = []
        self.endingIndex = None
        self.startIndex = None
        self.patternLength = None
        self.dframe = dframe

    def printList(self):
        for i in range(len(self.dframe)):
            print(i)

    def findPatterns(self):

        dframe = self.dframe
        length = len(dframe) // 2
        found = False
        start = 0

        while not found and length > 3:
            for n1 in range(0, len(dframe) - 2 * length + 1):
                for n2 in range(n1 + length, len(dframe) - length + 1):
                    ok = True
                    for i in range(0, length):
                        if dframe[n1 + i] != dframe[n2 + i]:
                            ok = False
                            break
                    if ok:
                        found = True
                        start = n1
                        break
                if found:
                    break
            if not found:
                length -= 1

        if found:
            # print("found sequence of length", length)
            # print("Start index: ", start, "Ending index: ", start + length + 1)
            self.startIndex = start
            self.endingIndex = start + length + 1
            self.patternLength = self.endingIndex - self.startIndex
            patternList = []
            for i in range(start, start + length + 1):
                # print("Pattern number: ", dframe[i])
                patternList.append(dframe[i])

            return patternList

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
    mido_obj.dump('MidiDumps/Melody_105-100_pitchSwap.midi')

    # reload for check
    # mido_obj_re = mid_parser.MidiFile('Melody_1.midi')
    # for note in mido_obj_re.instruments[0].notes:
    #     print(note)

path1 = "Data2/MELODY_100.csv"
path2 = "Data2/MELODY_105.csv"

df1 = pd.read_csv(path1, sep="\t", index_col=[0])
df2 = pd.read_csv(path2, sep="\t", index_col=[0])

df1pitchList = df1['pitch'].tolist()
df2pitchList = df2['pitch'].tolist()

patternObj1 = FindPattern(df1pitchList)
patternObj2 = FindPattern(df2pitchList)

patternList1 = patternObj1.findPatterns()
patternList2 = patternObj2.findPatterns()

print("---PATTERN 1---")
print(patternList1)
print("Start Index: ", patternObj1.startIndex)
print("Ending Index: ", patternObj1.endingIndex)
print("Pattern length: ", len(patternList1))

print("---PATTERN 2---")
print(patternList2)
print("Start Index: ", patternObj2.startIndex)
print("Ending Index: ", patternObj2.endingIndex)
print("Pattern length: ", len(patternList2))

df1pitchList_c = df1pitchList.copy()
df2pitchList_c = df2pitchList.copy()

# Swapping values from MELODY 105 with MELODY 100

for i in range(len(patternList2)):
    df1pitchList_c[patternObj1.startIndex + i] = df2pitchList_c[i]

print("TEST TO SEE IF LIST CHANGE WORKED: ", df1pitchList_c == df1pitchList)

df1pitchList_s = pd.Series(df1pitchList_c)

df2['pitch'] = df1pitchList_s

toMidi(df2)
