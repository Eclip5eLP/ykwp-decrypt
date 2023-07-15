import json
import os, sys, re

def isTranslatable(string):
	#return re.search('[a-zA-Z]', string)
	if string.isdigit() or string == "":
		return False
	return re.search('[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]', string)

# Parse json into easily editable json
def parseCud(file):
	if not os.path.isfile(file):
		print("File not found")
		return False

	# Read source file
	with open(file, 'r', encoding='utf-8') as f:
		data = json.load(f)

	# Check if valid
	try:
		if data["masterData"]:
			pass
	except Exception:
		print("File is not a valid cud")
		return False

	# Parse data
	translate = []
	try: # cud data is dictionary
		masterData = json.loads(data["masterData"])
		dbType = "dict"
		for i, x in enumerate(masterData["data"]):
			translate.append({"index":i,"charaName":x["charaName"],"messageText":x["messageText"]})
	except Exception: # cud data is string
		masterData = data["masterData"].split("|")
		dbType = "string"
		for i, x in enumerate(masterData):
			if isTranslatable(x):
				translate.append({"index":i,"text":x})

	# Save to parsed file
	with open(file.replace(".json", "_parsed.json"), 'w', encoding='utf-8') as f:
		json.dump({"type":dbType,"data":translate}, f, ensure_ascii=False)

# Merge parsed json data with original
def unparseCud(file):
	if not os.path.isfile(file):
		print("File not found")
		return False
	if not os.path.isfile(file.replace("_parsed.json", ".json")):
		print("Original file not found")
		return False

	# Read source and parsed files
	with open(file, 'r', encoding='utf-8') as f:
		data = json.load(f)

	with open(file.replace("_parsed.json", ".json"), 'r', encoding='utf-8') as f:
		masterDataRaw = json.load(f)

	# Check if valid
	try:
		if data["type"] == "dict":
			pass
	except Exception:
		print("Input is not parsed")
		return False

	# Parse data
	if data["type"] == "dict": # cud data is dictionary
		masterData = json.loads(masterDataRaw["masterData"])["data"]
		for i, x in enumerate(data["data"]):
			for idx, y in enumerate(x):
				if y == "index":
					continue
				masterData[x["index"]][y] = x[y]
		masterData = json.dumps({"data":masterData}, ensure_ascii=False)
	else: # cud data is string
		masterData = masterDataRaw["masterData"].split("|")
		for i, x in enumerate(data["data"]):
			masterData[x["index"]] = x["text"]
		masterData = '|'.join(masterData)

	# Save to source file
	with open(file.replace("_parsed.json", ".json"), 'w', encoding='utf-8') as f:
		f.write(json.dumps({"appVersion":masterDataRaw["appVersion"],"masterData":masterData}, ensure_ascii=False).replace("</R>", "<\\/R>"))

def main(file, mode):
	if mode == "-p":
		parseCud(file)
	elif mode == "-u":
		unparseCud(file)
	else:
		return False
	print("Done")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Syntax:\n" + sys.argv[0] + " <-p/-u> <file>")
		exit()
	main(sys.argv[2], sys.argv[1])