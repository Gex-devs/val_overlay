import socket
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
from flask import Flask
import asyncio
import websockets.server
from zeroconf import  ServiceInfo, Zeroconf

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

#ws = create_connection(f"ws://{sys.argv[1]}:{sys.argv[2]}")
#ws = create_connection("ws://192.168.1.22:4444")

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

connections = set()

# Create an asyncio queue to store messages.
message_queue = asyncio.Queue()

async def echo(websocket, path):
    # Add the websocket to the set of connections.
    try:

        connections.add(websocket)

    # Start a task to send messages from the queue to the server.
        #asyncio.create_task(send_messages(websocket, message_queue))
        asyncio.create_task(request_json())
        while True:
            message = await websocket.recv()

        #print messages
            print(message)
        # Send the message to all other connections.
            for ws in connections:
                if ws != websocket:
                    await ws.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed by client")
    except Exception as e:
        print("Unexpected error:", e)

# Send messages from the queue to the server.
async def send_messages(websocket, message_queue):
    while True:
        message = await message_queue.get()
        await websocket.send(message)
async def broadcast_message(message):
    for ws in connections:
        await ws.send(message)



async def request_json():
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
    
    
    await broadcast_message(responses2.text)

    original_party = responses2.json()
    while True:
        # Request the JSON data from the URL.
        live_querystring = {"cid":get_party_id()[0]}

        response = requests.request("GET", url, data=payload, headers=headers, params=live_querystring,verify=False)

        #print(response.text)

        second_response = response.json()

        f = jd.diff(original_chat,second_response,dump=True)

        if(f!="{}"):
            print("change was found")
            print(f)
            await broadcast_message(str(f))
            original_chat = second_response


        responses2_1 = requests.request("GET", url2, data=payload2, headers=headers2,verify=False)

        original_party_second_response = responses2_1.json()
        
        party_data_json_diff = jd.diff(original_party,original_party_second_response,dump=True)
        
        if(party_data_json_diff!="{}"):
            print(party_data_json_diff)
            logging.info('change was found')
            await broadcast_message(str(original_party_second_response))
            logging.info("Sent Party JSON")
            original_party = original_party_second_response

        '''
        response = requests.get("https://www.example.com/data.json")
        #data = response.json()

        # Convert the JSON data to a string and broadcast it to all clients.
        #message = json.dumps(data)
        await broadcast_message(message)
           '''
        # Wait for one second before requesting the JSON data again.
        await asyncio.sleep(1)
      
# Start the websocket server in a separate thread.
def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Start the request_json task.
    
    # Advertise the server using Bonjour.
    service_info = ServiceInfo(
    "_http._tcp.local.",
    f"{get_username(Player_ID)}._http._tcp.local.",
    address=socket.inet_aton("192.168.1.19"),
    port=8765,
    properties={},
    server="my-web-socket.local.",
    )

# Create a Zeroconf object and register the service
    zeroconf = Zeroconf()
    zeroconf.register_service(service_info)
    print("Server Started")
    start_server = websockets.serve(echo, "0.0.0.0", 8765)
    loop.run_until_complete(start_server)
    loop.run_forever()



def get_username(PUID):
    url = "https://pd.eu.a.pvp.net/name-service/v2/players"
    
    payload = [f"{PUID}"]
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("PUT", url, json=payload, headers=headers)

    print(response.json()[0]["GameName"])

    return response.json()[0]["GameName"]

def leave_party():


    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/players/{Player_ID}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("DELETE", url, data=payload, headers=headers)

    return response.status_code




def changeQ(qeue):
    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/queue"

    payload = {"queueID": qeue}

    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, json=payload, headers=headers,verify=False)

    return "ok"


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
    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}/quit"
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url=url, data=payload, headers=header,verify=False)

    return response.status_code


def select_agent(agent):

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}/select/{agent}"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(response.text)
    return agent


## Not sure about the request...check later
def lock_agent(agent):

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}/lock/{agent}"
    print(url)

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, data=payload, headers=headers,verify=False)

    return response.status_code

def party_accessibility(state):

    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/accessibility"

    payload = {"accessibility": f"{state}"}
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {Authorization}"
    }

    response = requests.request("POST", url, json=payload, headers=headers,verify=False)
    
    return response.status_code



def get_map():

    url = f"https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/{prematch_id()}"
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


def get_party_id():
    url = "https://glz-eu-1.eu.a.pvp.net/parties/v1/players/"+Player_ID

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "X-Riot-ClientVersion": "release-05.12-15-804337",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=header,verify=False)

    j = response.json()

    return j["CurrentPartyID"]+"@ares-parties.eu2.pvp.net",j["CurrentPartyID"]


def start_q():
    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/matchmaking/join"

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("POST", url, data=payload, headers=header)

    return response.status_code


def stop_q():
    url = f"https://glz-eu-1.eu.a.pvp.net/parties/v1/parties/{get_party_id()[1]}/matchmaking/leave"

    payload = ""
    header = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("POST", url, data=payload, headers=header)

    return response.status_code
 

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

    return response.status_code

def get_current_server_current_game():
    

    url = "https://glz-eu-1.eu.a.pvp.net/core-game/v1/matches/91181115-bfb5-40b3-841e-68fb5f12184b"

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=headers)

    if response.json()["GamePodID"] == "aresriot.aws-euc1-prod.eu-gp-frankfurt-1":
        server = "FrankFurt"
    elif response.json()["GamePodID"] == "aresriot.aws-apne1-prod.eu-gp-tokyo-1":
        server = "Tokyo"
    elif response.json()["GamePodID"] == "aresriot.aws-mes1-prod.eu-gp-bahrain-1":
        server = "Bahrain"
    elif response.json()["GamePodID"] == "aresriot.aws-rclusterprod-mad1-1.eu-gp-madrid-1":
        server = "Madrid"
    elif response.json()["GamePodID"] == "aresriot.aws-euw3-prod.eu-gp-paris-1":
        server = "Paris"
    elif response.json()["GamePodID"] == "aresriot.aws-eun1-prod.eu-gp-stockholm-1":
        server = "Stockholm"
    elif response.json()["GamePodID"] == "aresriot.mtl-riot-ist1-2.eu-gp-istanbul-1":
        server = "Istanbul"
    elif response.json()["GamePodID"] == "aresriot.aws-euw2-prod.eu-gp-london-1":
        server = "London"
    elif response.json()["GamePodID"] == "aresriot.aws-rclusterprod-waw1-1.eu-gp-warsaw-1":
        server = "Warsaw"

    return server


def pregame_gamemode():
    url = "https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/"+pre_game_matchID()

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=headers)

    return response.json()["QueueID"]


def get_current_server_pre_game():
    
    url = "https://glz-eu-1.eu.a.pvp.net/pregame/v1/matches/"+prematch_id()

    payload = ""
    headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    response = requests.request("GET", url, data=payload, headers=headers)

    if response.json()["GamePodID"] == "aresriot.aws-euc1-prod.eu-gp-frankfurt-1":
        server = "FrankFurt"
    elif response.json()["GamePodID"] == "aresriot.aws-apne1-prod.eu-gp-tokyo-1":
        server = "Tokyo"
    elif response.json()["GamePodID"] == "aresriot.aws-mes1-prod.eu-gp-bahrain-1":
        server = "bahrain"
    elif response.json()["GamePodID"] == "aresriot.aws-rclusterprod-mad1-1.eu-gp-madrid-1":
        server = "madrid"
    elif response.json()["GamePodID"] == "aresriot.aws-euw3-prod.eu-gp-paris-1":
        server = "paris"
    elif response.json()["GamePodID"] == "aresriot.aws-eun1-prod.eu-gp-stockholm-1":
        server = "stockholm"
    elif response.json()["GamePodID"] == "aresriot.mtl-riot-ist1-2.eu-gp-istanbul-1":
        server = "istanbul"
    elif response.json()["GamePodID"] == "aresriot.aws-euw2-prod.eu-gp-london-1":
        server = "london"
    elif response.json()["GamePodID"] == "aresriot.aws-rclusterprod-waw1-1.eu-gp-warsaw-1":
        server = "warsaw"

        
    return server

def current_game_state():
    
    current_game_url = "https://glz-eu-1.eu.a.pvp.net/core-game/v1/players/"+Player_ID

    current_game_payload = ""
    current_game_headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    current_game_response = requests.request("GET", current_game_url, data=current_game_payload, headers=current_game_headers)

    if(current_game_response.status_code == 200):
        return "In_Game"

    pre_game_url = "https://glz-eu-1.eu.a.pvp.net/pregame/v1/players/53f0e053-da42-5fe4-be34-326b738949a4"

    pre_game_payload = ""
    pre_game_headers = {
    "X-Riot-Entitlements-JWT": f"{Entitlment}",
    "Authorization": f"Bearer {Authorization}"
    }   

    pre_game_response = requests.request("GET", pre_game_url, data=pre_game_payload, headers=pre_game_headers)

    if(pre_game_response.status_code == 200):
        return "Agent_sel"
    
    return "MainMenu"


def Temp_Rest_Api():
    app = Flask(__name__) 

    @app.route("/current_state")
    def current_state():
        return current_game_state()
    @app.route("/get_name/<puid>")
    def retrun_as_name(puid):
        return get_username(puid)
    @app.route("/get_map")
    def return_map():
        return get_map()
    @app.route("/startQ")
    def start_matchmaking():
        return start_q()
    @app.route("/stopQ")
    def stop_matchmaking():
        return stop_q()
    @app.route("/leave_party")
    def leaveParty():
        return leave_party()
    @app.route("/Dodge")
    def skip_agentSel():
        return dodge_game()
    @app.route("/chat/<message>")
    def send_text(message):
        return send_chat(message)
    @app.route("/changeQ/<Queue>")
    def change_game_mode(Queue):
        return changeQ(Queue)
    @app.route("/party/<status>")
    def open_or_close_party(status):
        return party_accessibility(status)
    @app.route("/get_server/current_game")
    def game_server_current():
        return get_current_server_current_game()
    @app.route("/get_server/pre_game")
    def game_server_pre():
        return get_current_server_pre_game()
    @app.route("/get_gamemode/pre_game")
    def game_state_pre():
        return get_current_server_pre_game()
    @app.route("/select_agent/<agent>")
    def selection(agent):
        return select_agent(agent)
    @app.route("/lock_agent/<agent>")
    def lockON(agent):
        return lock_agent(agent)
    

    app.run(host="0.0.0.0",port=7979)






    



    



t3 = threading.Thread(target=Temp_Rest_Api)
server_thread = threading.Thread(target=start_server)

server_thread.start()
t3.start()
server_thread.join()
