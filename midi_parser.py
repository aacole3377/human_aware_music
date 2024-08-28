import miditoolkit
import pandas as pd
import mido
from miditoolkit.pianoroll import parser as pr_parser
from miditoolkit.pianoroll import utils
import os

path = "POP909/"

midi_obj_list = []
mido_obj_list = []
songID_list = []

""" song_id, start, end, pitch, velocity, duration, step """
""" song_id, time_signature, key_signature """

df = pd.DataFrame(columns=['song_id', 'start', 'end', 'pitch', 'velocity', 'duration', 'step', 'beat_Start', 'beat_End', 'beat_Duration'])
df2 = pd.DataFrame(columns=['song_id', 'time_signature', 'key_signature'])

for root_dir_path, sub_dirs, files in sorted(os.walk('POP909/')):
	# print("Root Directory path: ", root_dir_path)
	# print("Sub Directories: ", sub_dirs)
	# print("Files", files)
	for file in files:
		if file.endswith('.mid') and not file.__contains__("-"):
			path = os.path.join(root_dir_path, file)
			songID_list.append(file)
			with open(path):
				midi_obj_list.append(miditoolkit.midi.parser.MidiFile(path))

counter = 0
for k in midi_obj_list:
	currentInstrumentLength = (len(k.instruments))
	for i in range(currentInstrumentLength):
		startList = []
		endList = []
		velocityList = []
		pitchList = []
		durationList = []
		ticksPerBeatList = []
		beatList = []
		songName = "Midi_" + str(counter)
		for j in k.instruments[i].notes:
			startList.append(j.start)
			endList.append(j.end)
			velocityList.append(j.velocity)
			pitchList.append(j.pitch)
			file_name = k.instruments[i].name

		songID_list_s = pd.Series(songID_list)
		startList_s = pd.Series(startList)
		endList_s = pd.Series(endList)
		velocityList_s = pd.Series(velocityList)
		pitchList_s = pd.Series(pitchList)

		df['song_id'] = songName
		df['start'] = startList_s
		df['end'] = endList_s
		df['velocity'] = velocityList_s
		df['pitch'] = pitchList_s
		df['duration'] = endList_s - startList_s
		df['step'] = df['end'].shift(periods=1) - df['start']
		df['step'] = df['step'].abs()
		df['beat_Start'] = df['start'] / 480
		df['beat_End'] = df['end'] / 480
		df['beat_Duration'] = df['beat_End'] - df['beat_Start']

		# print(df.dtypes)
		# print(df)
		df.to_csv(os.path.join('Data/', file_name+str(counter)+'.csv'), sep='\t')
	counter += 1