import requests
import time
import jsondiff as jd
import os
import base64

import threading


def meme():
    print("who")

def ffs():
    while True:
        time.sleep(7)
        print("halo")

LockFile = open(os.getenv('LOCALAPPDATA') + "\Riot Games\Riot Client\Config\lockfile","r")
h = LockFile.read()
LockFilePort = h.split(":")[2]
message = "riot:"+LockFilePort
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_chat = base64_bytes.decode('ascii')


def mf():

    
    url = "https://127.0.0.1:12905/chat/v6/messages"

    querystring = {"cid":"0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net"}

    payload = ""

    headers = {"Authorization": f"Basic {base64_chat}"}

    responses = requests.request("GET", url, data=payload, headers=headers, params=querystring,verify=False)

    #print(response.text)

    orignal = responses.json()
    print("am i in the loop")

    while True:

        time.sleep(7)
        meme()
        url = "https://127.0.0.1:12905/chat/v6/messages"

        querystring = {"cid":"0ad005ea-a150-4db7-8e1a-6209bedf473a@ares-parties.eu2.pvp.net"}

        payload = ""
        headers = {"Authorization": f"Basic {base64_chat}"}

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring,verify=False)

    #print(response.text)

        second_response = response.json()

        f = jd.diff(orignal,second_response)

        if(f!={}):
            print("change was found")
            print(f)
            orignal = second_response
        
        continue


t1 = threading.Thread(target=ffs)
t2 = threading.Thread(target=mf)

t1.start()
    # starting thread 2
t2.start()
 
