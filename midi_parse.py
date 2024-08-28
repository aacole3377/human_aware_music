import miditoolkit
from miditoolkit.pianoroll import parser as pr_parser
from miditoolkit.pianoroll import utils
import os

path = "development/"
midi_obj_list = []

for filename in os.listdir(os.chdir(path)):
	with open(os.path.join(os.getcwd(), filename), 'r') as f:
		# print("--------------------------" + "\n" + "FILE NAME: " + filename)
		# print(miditoolkit.midi.parser.MidiFile(filename))
		midi_obj_list.append(miditoolkit.midi.parser.MidiFile(filename))

# Printing meta data
# Contains 6000 files
# for i in midi_obj_list:
# 	print(i)

# Note data
# for i in midi_obj_list[0].instruments[0].notes:
# 	print(i)

print(type(midi_obj_list[0].instruments[0].notes))

# Note data for all obj
with open('../output.txt', 'w') as wf:
	for i in range(len(midi_obj_list)):
		wf.write(str(midi_obj_list[i].instruments[0].notes))
		print(midi_obj_list[i].instruments[0].notes)

# Notes to piano roll
# pianoroll = pr_parser.notes2pianoroll(midi_obj_list[0].instruments[0].notes)
# print(pianoroll.shape)


