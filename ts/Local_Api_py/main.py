import sys
import time
from websocket import create_connection
import json
import requests
from Agents_id import *
import Agents_id
import os
import jsondiff as jd
import base64
import threading
import logging


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#ws = create_connection(f"ws://{sys.argv[1]}:{sys.argv[2]}")
ws = create_connection("ws://192.168.1.22:4444")
#ws = create_connection("ws://127.0.0.1:4444")
#ws.send("man just relpy")

requests.packages.urllib3.disable_warnings()

#file_current = __file__[:-7]

#f = open(rf'{file_current}Riot_Auth.json')

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
Player_ID = j["subject"]

def get_username(PUID):
    url = "https://pd.eu.a.pvp.net/name-service/v2/players"

    payload = [f"{PUID}"]
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("PUT", url, json=payload, headers=headers)

    #print(response.text)

    return response.json()[0]["GameName"]

def leave_party():


    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/players/{Player_ID}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("DELETE", url, data=payload, headers=headers)

   
    
def chat_messages():
    url = f"https://127.0.0.1:{LockFilePort}/chat/v6/messages"

    querystring ={"cid":get_party_id()[0]}

    payload = ""

    headers = {"Authorization": f"Basic {base64_chat}"}

    responses = requests.request("GET", url, data=payload, headers=headers, params=querystring,verify=False)

    #print(response.text)

    original_chat = responses.json()

    url2 = "https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/"+get_party_id()[1]

    payload2 = ""
    headers2 = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    responses2 = requests.request("GET", url2, data=payload2, headers=headers2,verify=False)

    print(responses2.text)

    ws.send(responses2.text)

    original_party = responses2.json()

    #print(responses2.text)

    while True:

        time.sleep(0.7)

        live_querystring = {"cid":get_party_id()[0]}

        response = requests.request("GET", url, data=payload, headers=headers, params=live_querystring,verify=False)

        #print(response.text)

        second_response = response.json()

        f = jd.diff(original_chat,second_response,dump=True)

        if(f!="{}"):
            print(type(f))
            print("change was found")
            print(f)
            ws.send(str(f))
            original_chat = second_response


        responses2_1 = requests.request("GET", url2, data=payload2, headers=headers2,verify=False)

        original_party_second_response = responses2_1.json()
        
        party_data_json_diff = jd.diff(original_party,original_party_second_response,dump=True)
        
        if(party_data_json_diff!="{}"):
            print(party_data_json_diff)
            logging.info('change was found')
            ws.send(str(original_party_second_response))
            logging.info("Sent Party JSON")
            original_party = original_party_second_response

        continue

def changeQ(qeue):
    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/queue"

    payload = {"queueID": qeue}

    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, json=payload, headers=headers,verify=False)

    print(response.status_code)


def prematch_id():
   
    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/players/{Player_ID}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("GET", url, data=payload, headers=headers,verify=False)

    jj = json.loads(response.text)
    print(response.text)
    return jj['MatchID']
    
   
def dodge_game():

    payload = ""
    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{pre_game_matchID()}/quit"
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url=url, data=payload, headers=header,verify=False)

    print(response)


def select(agent):

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}/select/{agent}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(response.text)


## Not sure about the request...check later
def lock_agent(agent):
    
    get_agent = getattr(Agents_id, agent)

    selected_agent = get_agent()

    print(selected_agent)


    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}/lock/{selected_agent}"
    print(url)

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, data=payload, headers=headers,verify=False)

    print(response.text)

def party_accessibility(state):

    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/accessibility"

    payload = {"accessibility": f"{state}"}
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, json=payload, headers=headers,verify=False)

print(response.text)
def check_agent(Agent):
    global current_agent
    if Agent == "Jett":
        select(jett())  ## Use this method instead and have a local variable to store the current selected agent for locking
        current_agent = "jett"
    elif Agent == "Omen":
        select(omen())
        current_agent = "omen"
    elif Agent == "Raze":
        select(raze())
        current_agent = "raze"
    elif Agent == "Sage":
        current_agent = "sage"
        select(sage())
    elif Agent == "Reyna":
        current_agent = "reyna"
        select(reyna())
    elif Agent == "Skye":
        current_agent = "skye"
        select(skye())

    elif Agent == "Killjoy":
        current_agent = "killjoy"
        select(killjoy())  ## Use this method instead and have a local variable to store the current selected agent for locking
    elif Agent == "Phx":
        current_agent = "phx"
        select(phx())
    elif Agent == "Brimstone":
        current_agent = "brimstone"
        select("9f0d8ba9-4140-b941-57d3-a7ad57c6b417")
    elif Agent == "Fade":
        current_agent = "fade"
        select(fade())
    elif Agent == "Cypher":
        current_agent = "cypher"
        select(cypher())
    elif Agent == "Viper":
        current_agent = "viper"
        select(viper())

    elif Agent == "Kayo":
        current_agent = "kayo"
        select(kayo())  ## Use this method instead and have a local variable to store the current selected agent for locking
    elif Agent == "Breach":
        current_agent = "breach"
        select(breach())
    elif Agent == "Astra":
        current_agent = "astra"
        select(astra())
    elif Agent == "Chamber":
        current_agent = "chamber"
        select(chamber())
    elif Agent == "Neon":
        current_agent = "neon"
        select(neon())
    elif Agent == "Sova":
        current_agent = "sova"
        select(sova())
    elif Agent == "Lock":
        print("Lock was detected")
        lock_agent(current_agent)
    elif Agent == "Dodge":
        print("Dodge Game")
        dodge_game()


def get_map():

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{pre_game_matchID()}"
    print(url)
    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=header)

    jj = json.loads(response.text)

    print(jj['MapID'])
    return jj['MapID']


def pre_game_matchID():
    payload = ""
    url = "https://glz-eu-1.eu.a.pvp.net/pregame/v1/players/"
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   
    response = requests.request("GET", f"{url}{Player_ID}", data=payload, headers=header)

    jj = json.loads(response.text)
    print("sucess")
    try:
        print(jj['MatchID'])
        return jj['MatchID']
    except KeyError:
        print("Match ID not found")
    
def get_party_id():
    url = "https://glz-eu-1.eu.a.pvp.net/parties/v1/players/"+Player_ID

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "X-Riot-ClientVersion": "release-05.10-11-796984",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=header,verify=False)

    j = json.loads(response.text)

    return j["CurrentPartyID"]+"@ares-parties.eu2.pvp.net",j["CurrentPartyID"]


def start_q():
    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/matchmaking/join"

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("POST", url, data=payload, headers=header)

    #print(response.status_code)


def stop_q():
    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/matchmaking/leave"

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("POST", url, data=payload, headers=header)

    #print(response.text)
 

def send_chat(text):
    url = f"https://127.0.0.1:{LockFilePort}/chat/v6/messages/"

    # get chat party
    payload = {
    "cid": get_party_id()[0],
    "message": text,
    "type": "groupchat"
    }
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {base64_chat}"
    }

    response = requests.request("POST", url, json=payload, headers=headers,verify=False)

    print(response.text)


def main():
    while True:
        result =  ws.recv()
        print(result)
        if result == "get_map":
            ws.send(get_map())
        if result == "Dodge":
            dodge_game()
        if result[:5] == "chat:":
            send_chat(result[5:])
        if result[:8] == "changeQ:":
            changeQ(result[8:])
        if result == "startQ":
            start_q()
        if result == "stopQ":
            stop_q()
        if result == "LeaveParty":
            leave_party()
        if result[:6] == "party:":
            party_accessibility(result[6:])
        check_agent(result)

    



    


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=chat_messages)

t1.start()
    # starting thread 2
t2.start()
 