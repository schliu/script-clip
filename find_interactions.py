import sys, os, glob, csv, string, re, json, csv, random
from datetime import datetime

data_dirname = "data"
input_filename = "trans_1.json"
output_filename = "interactions.csv"

with open(data_dirname + "/" + input_filename) as f:    
    data = json.load(f)

entries = []
for title, convo in data.iteritems():
	if "transcript" not in convo: continue
	hasStarted = False
	hasEnded = False
	numSeconds = 0
	inPoint = None
	outPoint = None
	officerSeconds = 0
	for line in convo["transcript"]:
		if hasStarted and "meta" in line and "returns to " in line["meta"].lower(): break
		if "start" not in line or "end" not in line: continue
		if not hasStarted:
			if "meta" in line and "to dispatch" in line["meta"].lower(): continue
			if "OFFICER" not in line["speaker"]: continue
			hasStarted = True
			inPoint = line["start"]
		if hasEnded: break
		start = datetime.strptime(line["start"], "%H:%M:%S")
		end = datetime.strptime(line["end"], "%H:%M:%S")
		if ((start - datetime.strptime(inPoint, "%H:%M:%S")).total_seconds() > 30):
			break
		outPoint = line["end"]
		duration = (end - start).total_seconds()
		if "OFFICER" in line["speaker"]:
			officerSeconds += duration
		numSeconds += duration
		if numSeconds >= 30: break
	if officerSeconds < 10: continue
	race = convo["SDRace"] if "SDRace" in convo else ""
	entries.append((title, race, inPoint, outPoint))
random.shuffle(entries)

with open(data_dirname + "/interactions.csv", 'wb') as f:
	wr = csv.writer(f, quoting=csv.QUOTE_ALL)
	wr.writerows(entries)