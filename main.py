import pyautogui
import time, os
from pynput.mouse import Button, Controller
from directkeys import PressKey, ReleaseKey, TAB
from screenSize import GetScreenSize

_betCounter = 1
SCREEN_SIZE = GetScreenSize()
SCREEN_STRING = str(SCREEN_SIZE[0]) + "x" + str(SCREEN_SIZE[1])
MOUSE = Controller()

def startup():
    if os.path.exists("pics/bet" + SCREEN_STRING + ".png") == False:
        print("Kein Referenzbild für aktuelle Screen-Size gefunden: " + SCREEN_STRING +"px")
        exit()
    print("Casino-Bot is starting...")

    while(True):
        while(findBetField() == False):
            print("Konnte Tisch nicht finden...")
            time.sleep(5)


        while(detectWinOrLose() == False):
            print("Runde läuft momentan...")
            time.sleep(2)

    exit()

def findBetField():
    try:
        point= pyautogui.locateCenterOnScreen(f'pics/bet{SCREEN_STRING}.png', confidence=0.8)
        print("Tisch gefunden!")
        moveMouseTo(point[0], point[1])

        PressKey(TAB)
        time.sleep(1)
        ReleaseKey(TAB)

        time.sleep(1)
        for i in range(_betCounter):
           print("mouse clicking...")
           MOUSE.press(Button.left)
           time.sleep(1)
           MOUSE.release(Button.left)
           time.sleep(1)
        return True
    except:
        return False

def detectWinOrLose():
    try:
        x, y= pyautogui.locateCenterOnScreen(f'pics/win{SCREEN_STRING}.png', confidence=0.8)
        _betCounter = 1
        print("Gewonnen! Bet-Counter auf 1 gesetzt")
    except:
        try:
            x,y = pyautogui.locateCenterOnScreen(f'pics/lose{SCREEN_STRING}.png', confidence=0.8)
            _betCounter*=2
            print("Verloren! Bet-Counter verdoppelt auf " + _betCounter)
        except:
            return False
    return True

def moveMouseTo(x, y):
    offsetX = 350
    offsetY = 300
    pyautogui.moveTo((x-offsetX), (y+offsetY), duration = 3)
    print(f"debug: mouse moved to ({(x-offsetX)},{(y+offsetY)})")


if __name__ == "__main__":
    startup()

#maus auf rot -> max einsatz -> einsatz-counter abarbeiten (place orders)
#detection for win/lose -> einsatz-counter verdoppeln oder zurücksetzen

