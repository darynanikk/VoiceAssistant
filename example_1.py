import pyautogui
from word2number import w2n


#hello backspacepyautogui.hotkey('ctrl', 'shift', 'esc')

pyautogui.hotkey("ctrl", "a")

map = {
    "control a" : ["ctrl", "a"]
}

pyautogui.hotkey(*map.get("control a"))
hellohello

hello