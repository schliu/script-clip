import sys, os, glob, csv, string, re, json

old_filename = sys.argv[1]
dirname = "data"
new_filename = dirname + "/trans_1.json"

regex = r', \"utterance\": \".*?[^\\]+?\"'

old_f = open(old_filename, 'r')
new_f = open(new_filename, 'w')

text = old_f.read()
(text, num) = re.subn(regex, '', text, count=0)

stops = json.loads(text)
parsed = {}

for id, val in stops.iteritems():
	parsed[id] = {x: val[x] for x in ("SDRace", "FileLocation", "transcript") if x in val}
	#entry = {}
	#if "SDRace" in val: entry["SDRace"] = val["SDRace"]
	#if "FileLocation" in val: entry["FileLocation"] = val["FileLocation"]
	#if "transcript" in val: entry["transcript"] = val["transcript"]
	#parsed[id] = entry

json.dump(parsed, new_f)