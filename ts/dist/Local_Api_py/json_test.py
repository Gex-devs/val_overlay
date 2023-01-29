
import os,requests,base64,json



LockFile = open(os.getenv('LOCALAPPDATA') + "\Riot Games\Riot Client\Config\lockfile","r")
h = LockFile.read()
LockFilePort = h.split(":")[2]
LockFilePassword = h.split(":")[3]

message = "riot:"+LockFilePassword
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_chat = base64_bytes.decode('ascii')


url = f"https://127.0.0.1:{LockFilePort}/entitlements/v1/token"

payload = ""
headers = {"Authorization": f"Basic {base64_chat}"}

response = requests.request("GET", url, data=payload, headers=headers,verify=False)


j = json.loads(response.text)

    

Entitlment = j["token"]
Authorization = j["accessToken"]