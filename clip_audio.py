import sys, os, glob, csv, string, re, json, csv, random
from datetime import datetime
import scipy.io.wavfile
import numpy as np

data_dirname = "data"
input_filename = "interactions_lite.csv"

with open(data_dirname + "/" + input_filename, "rb") as f:
	reader = csv.reader(f)
	for row in reader:
		filename = row[0]
		inPoint = (datetime.strptime(row[2], "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S")).total_seconds()
		outPoint = (datetime.strptime(row[3], "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S")).total_seconds()

		rate, data = scipy.io.wavfile.read(data_dirname + "/audio_input/" + filename)
		clip = np.ceil(np.array([[inPoint, outPoint + 1]]) * rate)
		result = []
		for time in clip:
			start = time[0]
			end = time[1]
			if start >= data.shape[0]:
				start = data.shape[0]-1
			if end >= data.shape[0]:
				end = data.shape[0]-1
			result.extend(data[start:end])

		if not os.path.exists(data_dirname + "/audio_output/" + filename):
			os.makedirs(data_dirname + "/audio_output/" + filename)
		scipy.io.wavfile.write(data_dirname + "/audio_output/" + filename + "/" + filename + "_" + row[2] + "_" + row[3], rate, np.array(result))