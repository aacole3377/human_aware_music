import miditoolkit
import pandas as pd
import mido
import numpy as np
import collections
from miditoolkit.midi import parser as mid_parser
from miditoolkit.midi import containers as ct
from difflib import SequenceMatcher
import math
import os


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

def pattern(seq):
    storage = {}
    for length in range(1, int(len(seq) / 2) + 1):
        valid_strings = {}
        for start in range(0, len(seq) - length + 1):
            valid_strings[start] = tuple(seq[start:start + length])
        candidates = set(valid_strings.values())
        if len(candidates) != len(valid_strings):
            print("Pattern found for " + str(length))
            storage = valid_strings
        else:
            print("No pattern found for " + str(length))
            break
    return set(v for v in storage.values() if list(storage.values()).count(v) > 1)

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
    mido_obj.dump('MidiDumps/Melody_1.midi')

    # reload for check
    # mido_obj_re = mid_parser.MidiFile('Melody_1.midi')
    # for note in mido_obj_re.instruments[0].notes:
    #     print(note)


path0 = 'Data2/MELODY_1.csv'
path1 = 'Data2/MELODY_2.csv'
path2 = 'Data2/MELODY_3.csv'
path3 = 'Data2/MELODY_6.csv'

dfList = []

df0 = pd.read_csv(path0, sep='\t', index_col=[0])
df1 = pd.read_csv(path1, sep='\t', index_col=[0])
df2 = pd.read_csv(path2, sep='\t', index_col=[0])
df3 = pd.read_csv(path3, sep='\t', index_col=[0])

dfList.append(df0)
dfList.append(df1)
dfList.append(df2)
dfList.append(df3)

midi1StartToList = df2['start'].tolist()
midi1EndToList = df2['end'].tolist()
midi2StartToList = df3['start'].tolist()
midi2EndToList = df3['end'].tolist()

midi1DurationToList = df2['duration'].tolist()
midi2DurationToList = df3['duration'].tolist()

# Pattern object for df2

midi1DurationObj = FindPattern(midi1DurationToList)
midi1DurationPatList = midi1DurationObj.findPatterns()
midi1_startIndex = midi1DurationObj.startIndex
Midi1_endIndex = midi1DurationObj.endingIndex

print("Printing pattern 1: ", midi1DurationPatList)
print("Starting index for pattern 1: ", midi1_startIndex)
print("Ending index for pattern 1: ", Midi1_endIndex)
print("Length of pattern 1: ", midi1DurationObj.patternLength)

# Pattern object for df3

midi2DurationObj = FindPattern(midi2DurationToList)
midi2DurationPatList = midi2DurationObj.findPatterns()
midi2_startindex = midi2DurationObj.startIndex
midi2_endIndex = midi2DurationObj.endingIndex

print("Printing pattern 2: ", midi2DurationPatList)
print("Starting index for pattern 2: ", midi2_startindex)
print("Ending index for pattern 2: ", midi2_endIndex)
print("Length of pattern 2: ", midi2DurationObj.patternLength)

# Copies to test changes in list later

midi1StartToList_c = midi1StartToList.copy()
midi1EndToList_c = midi1EndToList.copy()
midi2StartToList_c = midi2StartToList.copy()
midi2EndToList_c = midi2EndToList.copy()

# Replace values

for i in range(midi2DurationObj.patternLength):
    midi1StartToList_c[i] = midi2StartToList[midi2_startindex + i]
    midi2EndToList_c[i] = midi2EndToList[midi2_startindex + i]

print("Testing new list for start...", midi1StartToList_c == midi1StartToList)
print("Testing new list for end...", midi2EndToList_c == midi2EndToList)

dfStartToList_s = pd.Series(midi1StartToList_c)
df2['start'] = dfStartToList_s

toMidi(df2)

