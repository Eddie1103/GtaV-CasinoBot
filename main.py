import pyautogui
import time

_amount = 1000
_betCounter = 1

def startup():
    print("Casino-Bot is starting...")
    
    exit()

def findBetField():
    x, y= pyautogui.locateCenterOnScreen("redbet.png", region=(980,630,100,60))
    pyautogui.moveTo(x, y, duration = 3)
    pyautogui.press("tab")
    time.sleep(0.5)
    for i in range(_betCounter):
        pyautogui.leftClick()
        time.sleep(1)

def detectWinOrLose():
    x, y= pyautogui.locateCenterOnScreen("win.png", region=(0,0,370,90))
    if x == None:
        x,y = pyautogui.locateCenterOnScreen("lose.png", region=(0,0,370,90))
        if x == None:
            return False
        else:
            _betCounter+1
    else:
        _betCounter = 1
    #e region=(0,0,370,90)
    print("")
    return True

def moveMouseTo(x, y):
    pyautogui.moveTo(100, 100, duration = 5)
    print("debug: mouse moved to ({x}, {y})")


if __name__ == "__main__":
    startup()

#maus auf rot -> max einsatz -> einsatz-counter abarbeiten (place orders)
#detection for win/lose -> einsatz-counter verdoppeln oder zurücksetzen

