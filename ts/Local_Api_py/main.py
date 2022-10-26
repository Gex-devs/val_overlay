import time
from websocket import create_connection
from Riot_AuthFlow import Auth_Riot
import json
import requests
from Agents_id import *
import Agents_id

ws = create_connection("ws://192.168.1.23:4444")
#ws = create_connection("ws://127.0.0.1:4444")
#ws.send("man just relpy")



## Theortically this should work



file_current = __file__[:-7]

f = open(rf'{file_current}Riot_Auth.json')
j = json.load(f)

Entitlment = j["Riot_Auth"][0]["Entitlment_token"]
Authorization = j["Riot_Auth"][0]['Acess_Token']
Player_ID = j["Riot_Auth"][0]['PUUID']



def prematch_id():
   

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/players/{Player_ID}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    jj = json.loads(response.text)
    print(response.text)
    return jj['MatchID']
    
   

def select(agent):

    Auth_Riot()

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}/select/{agent}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
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

    response = requests.request("POST", url, data=payload, headers=headers)

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

while True:
    result =  ws.recv()
    print(result)
    check_agent(result)



    

