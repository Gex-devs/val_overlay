
import pyautogui
import time


pyautogui.FAILSAFE = False
def keyboard_left_right():
    while True:
        pyautogui.typewrite('a')

time.sleep(3)
keyboard_left_right()