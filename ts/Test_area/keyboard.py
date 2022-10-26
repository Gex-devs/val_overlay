import pyautogui



pyautogui.FAILSAFE = False
def keyboard_left_right():
    while True:
        pyautogui.typewrite('a')


keyboard_left_right()