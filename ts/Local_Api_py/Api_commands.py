import requests
import json
import Agents_id
from Riot_AuthFlow import Auth_Riot


## Theortically this should work

Auth_Riot()

file_current = __file__[:-15]

f = open(rf'{file_current}Riot_Auth.json')
j = json.load(f)

Entitlment = j["Entitlment_token"]
Authorization = j['Acess_Token']


def prematch_id():
   

    url = "https://glz-eu-1.eu.a.pvp.net/pregame/v1/players/26cfe588-06fa-5d09-95e7-4761c684f790"

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

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/f{prematch_id()}/lock/{selected_agent}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)


def dodge_game():

    payload = ""

    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", "/pregame/v1/matches/4124124/quit", payload, headers)