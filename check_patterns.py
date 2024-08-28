import pandas as pd
import numpy as np
import os

class FindPattern:
    def __init__(self, dframe):
        self.patternList = []
        self.endingIndex = None
        self.startIndex = None
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
            patternList = []
            for i in range(start, start + length + 1):
                # print("Pattern number: ", dframe[i])
                patternList.append(dframe[i])

            return patternList

dflist = []

for root_dir_path, sub_dirs, files in sorted(os.walk('/Users/aaron/Desktop/School/IndependentStudies/AI_music/MidiDumps/generated_csv')):
    for file in files:
        print(file)
        if file.endswith('.csv'):
            path = os.path.join(root_dir_path, file)
            with open(path):
                dflist.append(pd.read_csv(path, sep='\t', index_col=[0]))

objectList = []
pitchList = []
patternList = []


for a in dflist:
    pitchList.append(a['pitch'].tolist())

for i in pitchList:
    objectList.append(FindPattern(i))

for j in objectList:
    patternList.append(j.findPatterns())

print()

for k in patternList:
    print(k)