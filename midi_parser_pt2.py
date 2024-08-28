import miditoolkit
import pandas as pd
import mido
from miditoolkit.pianoroll import parser as pr_parser
from miditoolkit.pianoroll import utils
import os

path = "POP909/"

chordsList = []
dfList = []
counter = 0
for root_dir_path, sub_dirs, files in sorted(os.walk('POP909/')):
	for file in files:
		songName = "Midi_" + str(counter)
		counter += 1
		if file.__contains__('chord_audio.txt'):
			path = os.path.join(root_dir_path, file)
			df = pd.read_csv(path, sep='\t', header=None)
			df.columns = ['Start', 'End', 'Chords']
			df['song_id'] = songName
			df.pop('song_id')
			dfList.append(df)
			df.to_csv(os.path.join('Chords/', 'chord_audio_' + str(counter) + '.csv'), sep='\t')


