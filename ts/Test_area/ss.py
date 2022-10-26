from threading import Thread
import time
from websocket import create_connection
ws = create_connection("ws://192.168.1.22:4444")
#ws = create_connection("ws://127.0.0.1:4444")
ws.send("man just relpy")

while True:
    result =  ws.recv()
    print(result)
ws.close()
