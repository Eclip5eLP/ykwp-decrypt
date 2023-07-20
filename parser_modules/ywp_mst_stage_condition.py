import re

def parser(data, dbType):
	translate = []
	if dbType == "dict": # cud data is dictionary
		masterData = json.loads(data)
		for i, x in enumerate(masterData["data"]):
			translate.append({"index":i,"charaName":x["charaName"],"messageText":x["messageText"]})
	else: # cud data is string
		masterData = data.split("^")
		for i, x in enumerate(masterData):
			if isTranslatable(x):
				translate.append({"index":i,"text":x})
	return translate

def unparser(data, masterDataRaw, dbType):
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
	except Exception as e:
		print("Invalid data")
		print(e)
		return False

def isTranslatable(string):
	if string.isdigit() or string == "":
		return False
	jp = re.search('[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff66-\uff9f]', string)
	en = re.search('[a-zA-Z]', string)
	if jp or en:
		return True
	return False