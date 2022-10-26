import asyncio
import subprocess
import sys
from time import time
import websockets
import pyautogui
import time
import serial


arduino = serial.Serial(port='COM7', baudrate=9600, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

duplicate = 0




async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)
        print(message)
        if message == "death":
            write_read("L")
           
     
            

            
        

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, '127.0.0.1', 8765))
asyncio.get_event_loop().run_forever()

