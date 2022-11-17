
import time
from websocket import create_connection
from Riot_AuthFlow import Auth_Riot
import json
import requests
from Agents_id import *
import Agents_id

ws = create_connection("ws://192.168.1.22:4444")
#ws = create_connection("ws://127.0.0.1:4444")
#ws.send("man just relpy")







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
    
   
def dodge_game():

    payload = ""
    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{pre_game_matchID()}/quit"
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url=url, data=payload, headers=header)

    print(response)

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
    
def get_party():
    url = "https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/c96e2e90-994a-4b11-9f61-2876e9b7aed9"

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=header)

    print(response.text)

def start_q():
    url = "https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/c96e2e90-994a-4b11-9f61-2876e9b7aed9/matchmaking/join"

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("POST", url, data=payload, headers=header)

    print(response.text)


def stop_q():
    url = "https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/c96e2e90-994a-4b11-9f61-2876e9b7aed9/matchmaking/leave"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": "eyJraWQiOiJrMSIsImFsZyI6IlJTMjU2In0.eyJlbnRpdGxlbWVudHMiOltdLCJhdF9oYXNoIjoiOGRRZmN3Q01Ma2lyb3BVN3c4d0dzdyIsInN1YiI6IjZkYWZmM2JlLTkyZDgtNThjYi05ODZjLWU0YWI3MmI5NmE1YSIsImlzcyI6Imh0dHBzOlwvXC9lbnRpdGxlbWVudHMuYXV0aC5yaW90Z2FtZXMuY29tIiwiaWF0IjoxNjY3NDQyMDY0LCJqdGkiOiJ5WnF3c0VUQlliUSJ9.Thq4Jl1qhNnBMA7bySRs8QSgQXg04n3bSX2MLlnJSmR63VICp4a2F59ajjAiyf351YPlHPXIMWw4TUFA2ocHM99HX9EJoBHgcEQ3p-Ta7ol0WfdFLmJHVvNFBwn3e1rVAirTHJFe3YMPdwaSBNsKNPnpVn4wapuPjkLSehL7vZgKChvAh8mOP8AsLhd62RPaaJ1bkvrM6BZS_bz6mpuZ_V2gy9AxQ6pP-mSif1dAMRKKYJBdgnASaqoFhX4XptVZA-W17xgKVmq2WNxW8FAAUlwoMUyb9_mqZMW8WqSZdbYEzE2nbdxaKIX3cQUDmKCspLTNrlOvrgU_i5qEH-TFiw",
    "Authorization": "Bearer eyJraWQiOiJzMSIsImFsZyI6IlJTMjU2In0.eyJwcCI6eyJjIjoiZXUifSwic3ViIjoiNmRhZmYzYmUtOTJkOC01OGNiLTk4NmMtZTRhYjcyYjk2YTVhIiwic2NwIjpbImFjY291bnQiLCJvcGVuaWQiXSwiY2xtIjpbImZlZGVyYXRlZF9pZGVudGl0eV9wcm92aWRlcnMiLCJlbWFpbF92ZXJpZmllZCIsIm9wZW5pZCIsInB3IiwicmduX0VVVzEiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiLCJhY2N0X2dudCIsImxvY2FsZSIsImFjY3QiLCJhZ2UiLCJhY2NvdW50X3ZlcmlmaWVkIiwiYWZmaW5pdHkiXSwiZGF0Ijp7InAiOm51bGwsInIiOiJFVVcxIiwiYyI6ImVjMSIsInUiOjI1MDUzNjgzMzc2MzA3MjAsImxpZCI6IkxGYWZlSUl0MUZoOXYwenBIWUFwZ3cifSwiaXNzIjoiaHR0cHM6XC9cL2F1dGgucmlvdGdhbWVzLmNvbSIsImV4cCI6MTY2NzQ0NTY2MywiaWF0IjoxNjY3NDQyMDYzLCJqdGkiOiJ5WnF3c0VUQlliUSIsImNpZCI6InBsYXktdmFsb3JhbnQtd2ViLXByb2QifQ.X40gllEHkB-tqo69YjuXz_MDenMfHWeNUwmlhacXuGEiBKAVgSkzYSWuYZdwbuAqPnS6muvAM7co6yQ5kzRQpRNyLmXV6fOvtXawzuWsYjhwPJFTYC2-GjYe784LeejSa1xrJ83k6tzVw3Vtgot7LN1wZwOhq7GbUBkXh8Y6F5E"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)


while True:

    result =  ws.recv()
    print(result)
    if result == "get_map":
        ws.send(get_map())
    if result == "Dodge":
        dodge_game()
    check_agent(result)
    



    

