import json
import re

filename = "D:\\DATA\\chall\\natas\\scripts\\natas.json"

def updateLevelsDict(levelsList):
	'''
		Update jsonContent object with updated levels list
	'''
	jsonContent = openFile(filename)
	jsonContent["levels"] = levelsList
	return jsonContent

def getLevelsList():
	'''
		Extract the level ist in the jsonContent

		return :
			- a list containing levels (that are also a list)
	'''
	jsonContent = openFile(filename)
	levelsList = jsonContent["levels"]
	return levelsList

def checkLevel(n):
	"""
		Check if a level, identified by its name, exists
		
		return :
			- Boolean

		call example : 
			chechLevel(1)

	"""
	levelsList = getLevelsList()
	levelExists = False
	for level in levelsList:
		if "natas"+str(n) == level["name"]:
			levelExists = True
			break
		
	return levelExists

def openFile(f):
	'''
		Get the json data in file passed in parameter
		return :
			- json data (a list)
	'''
	with open(f, "r") as handle:
		jsonData = json.load(handle)
	return jsonData

def saveFile(f, jsonObject):
	'''
		Save jsonObject (listLevel) in the file passed in parameter.
		return :
			- nothing
	'''

	finalJson = updateLevelsDict(jsonObject)
	with open(f, 'w') as outfile:  
   		json.dump(finalJson, outfile)

def updateLevel(n, password):
	'''
		Create or update level information. Modify the levelsList list and then call the saveFile function
		input : 
			- n : int, level number to update
			- password
		call example : 
			updateLevel(1, "SQJKMDLJKQSD")
	'''
	levelsList = getLevelsList()
	if checkLevel(n):
		i = 0
		for level in levelsList:
			if "natas"+str(n) == level["name"]:
				newLevel = {'name': 'natas'+str(n), 'url': 'http://natas'+str(n)+'.natas.labs.overthewire.org/', 'username': 'natas'+str(n), 'password': password}
				levelsList[i] = newLevel
				break
			i += 1
		
	else:
		newLevel = {'name': 'natas'+str(n), 'url': 'http://natas'+str(n)+'.natas.labs.overthewire.org/', 'username': 'natas'+str(n), 'password': password}
		levelsList.append(newLevel)

	saveFile(filename, levelsList)

def getLevel(n):
	'''
		get level information from levelsList and return it
		return :
			- level information (a list)

		call example : 
			currentLevel = getLevelsList(18)
			print(currentLevel)
	'''

	levelsList = getLevelsList()
	for level in levelsList:
		if "natas"+str(n) == level["name"]:
			return level


def initLevel(n):
	if checkLevel(n):
		currentLevel = getLevel(n)
	else:
		updateLevel(n, "X")	
		currentLevel = getLevel(n)

	print("\n==> Level : "+currentLevel["name"])

	user = currentLevel["username"]

	# variable setting
	if currentLevel["name"] == "natas0":
		password = "natas0"
	else : 
		password = currentLevel["password"]
	url = currentLevel["url"]

	return user, password, url

def findPasswordInString(s):
	"""
		Try to find password in a string based on regex (32 char long string)
		return
			- Booelan
			- string ("X" or password found)
	"""
	passFound = False
	password = "X"
	challPasswords = re.search('([A-Za-z0-9]{32})', s)
	if challPasswords:
		passFound = True	
		password = str(challPasswords.group(1))
	return passFound,password