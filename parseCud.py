import json
import os, sys, re
sys.path.append('./parser_modules')

# Check if text is translatable
def isTranslatable(string):
	if string.isdigit() or string == "":
		return False
	return re.search('[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]', string)

# Load a module and use it to parse
def moduleParser(moduleName, data, masterData, dbType, mode):
	fname, file_extension = os.path.splitext(moduleName)
	if not os.path.isfile('./parser_modules/' + fname + ".py"):
		return False
	module = __import__(fname)
	print("Using " + fname + " module")
	try:
		if mode == 0: # Parse
			return module.parser(data, dbType)
		elif mode == 1: # Unparse
			return module.unparser(data, masterData, dbType)
		else: # Invalid
			return False
	except Exception as e:
		print("Module error:")
		print(e)
		return False

# Default parsing method
def parser_default(data, dbType):
	translate = []
	if dbType == "dict": # cud data is dictionary
		masterData = json.loads(data)
		for i, x in enumerate(masterData["data"]):
			translate.append({"index":i,"charaName":x["charaName"],"messageText":x["messageText"]})
	else: # cud data is string
		masterData = data.split("|")
		for i, x in enumerate(masterData):
			if isTranslatable(x):
				translate.append({"index":i,"text":x})
	return translate

# Default unparsing method
def unparser_default(data, masterDataRaw, dbType):
	try:
		if dbType == "dict": # cud data is dictionary
			masterData = json.loads(masterDataRaw)["data"]
			for i, x in enumerate(data):
				for idx, y in enumerate(x):
					if y == "index":
						continue
					masterData[x["index"]][y] = x[y]
			masterData = json.dumps({"data":masterData}, ensure_ascii=False)
		else: # cud data is string
			masterData = masterDataRaw.split("|")
			for i, x in enumerate(data):
				masterData[x["index"]] = x["text"]
			masterData = '|'.join(masterData)
		return masterData
	except Exception:
		print("Invalid data")
		return False

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

	# Check data type
	try: # dict
		masterData = json.loads(data["masterData"])
		dbType = "dict"
	except Exception: # string
		dbType = "string"

	# Parse data
	# Modulated parsing
	parsed = moduleParser(os.path.basename(file), data["masterData"], None, dbType, 0)
	if parsed != False:
		masterData = parsed
	else:
		masterData = parser_default(data["masterData"], dbType)

	# Save to parsed file
	with open(file.replace(".json", "_parsed.json"), 'w', encoding='utf-8') as f:
		json.dump({"type":dbType,"data":masterData}, f, ensure_ascii=False, separators=(',', ':'), indent=4)

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
		if data["type"] == "":
			print("Invalid data type")
	except Exception:
		print("Input is not parsed")
		return False

	# Parse data
	# Modulated parsing
	parsed = moduleParser(os.path.basename(file.replace("_parsed.json", ".json")), data["data"], masterDataRaw["masterData"], data["type"], 1)
	if parsed != False:
		masterData = parsed
	else:
		masterData = unparser_default(data["data"], masterDataRaw["masterData"], data["type"])

	# Save to source file
	with open(file.replace("_parsed.json", ".json"), 'w', encoding='utf-8') as f:
		f.write(json.dumps({"appVersion":masterDataRaw["appVersion"],"masterData":masterData}, ensure_ascii=False, separators=(',', ':')).replace("</R>", "<\\/R>").replace("</B>", "<\\/B>"))

# Main
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