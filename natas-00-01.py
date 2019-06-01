import requests
from requests.auth import HTTPBasicAuth
import re
import natas

challNumber = 0
user, password, url = natas.initLevel(challNumber)

print("[+] Request to "+url)
# request to the URL with BasicAuth
res = requests.get(url, auth=HTTPBasicAuth(user, password))

# Try to find "password" in response text
print("[+] Trying to find a password in server's response...")
resTab = res.text.split('\n')
for line in resTab:
	if "password" in line :
		print("\"password\" string found here : "+ line)
		b, p = natas.findPasswordInString(line)
		if b:
			print("[+] Password found ! ["+str(p)+"] ")
			natas.updateLevel(challNumber + 1 , p)
			print("[+] Level "+str(challNumber + 1)+" updated")

challNumber = 1
user, password, url = natas.initLevel(challNumber)

print("[+] Request to "+url)
# request to the URL with BasicAuth
res = requests.get(url, auth=HTTPBasicAuth(user, password))

# Try to find "password" in response text
print("[+] Trying to find a password in server's response...")
resTab = res.text.split('\n')
for line in resTab:
	if "password" in line :
		print("\"password\" string found here : "+ line)
		b, p = natas.findPasswordInString(line)
		if b:
			print("[+] Password found ! ["+str(p)+"] ")
			natas.updateLevel(challNumber + 1, p)
			print("[+] Level "+str(challNumber + 1)+" updated")
