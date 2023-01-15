import requests
import os
import json

print()

f = open(os.getenv('LOCALAPPDATA') + "\Riot Games\Riot Client\Config\lockfile","r")

h = f.read()

port = h.split(":")[2]

url = f"https://127.0.0.1:{port}/entitlements/v1/token"

payload = ""
headers = {"Authorization": "Basic cmlvdDo5VWU0dUV3NWhlS2hzZEUyQjJKNTBR"}

response = requests.request("GET", url, data=payload, headers=headers,verify=False)

#print(response.text)

js = json.loads(response.text)


print(js["accessToken"])