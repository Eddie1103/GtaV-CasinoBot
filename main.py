import pyautogui
import time, os
from screenSize import GetScreenSize

_betCounter = 1
SCREEN_SIZE = GetScreenSize()
SCREEN_STRING = str(SCREEN_SIZE[0]) + "x" + str(SCREEN_SIZE[1])

def startup():
    if os.path.exists("pics/bet" + SCREEN_STRING + ".png") == False:
        print("Kein Referenzbild für aktuelle Screen-Size gefunden: " + SCREEN_STRING +"px")
        exit()
    print("Casino-Bot is starting...")

    while(True):
        while(findBetField() == False):
            print("Konnte Tisch nicht finden...")
            time.sleep(5)
            '''
        while(detectWinOrLose() == False):
            print("Runde läuft momentan...")
            time.sleep(2)
            '''

    exit()

def get_jetons_coords():
    coords = pyautogui.locateCenterOnScreen(f'pics/jetons{SCREEN_STRING}.png', confidence=0.8)
    return coords

def findBetField():
    # try:
    #pyautogui.screenshot(imageFilename="test.png", region=(980,630,100,60))
    coords = pyautogui.locateCenterOnScreen(f'pics/bet{SCREEN_STRING}.png', confidence=0.8)
    if coords == None:
        return False
    print(coords)
    coordsJetons = get_jetons_coords()
    if coordsJetons == None:
        return False
    while coordsJetons != coords:
        print(coordsJetons)
        # calculate offset from jetons to betfield and move cursor by offset
        offset = (coords[0] - coordsJetons[0], coords[1] -  coordsJetons[1])
        currentMousePos = pyautogui.position()
        pyautogui.moveTo(currentMousePos[0] + offset[0], currentMousePos[1] + offset[1])
        coordsJetons = get_jetons_coords()
        if coordsJetons == None:
            return False
        time.sleep(0.5)
    pyautogui.press("tab")
    time.sleep(0.5)

    return False
    for i in range(_betCounter):
        pyautogui.leftClick()
        time.sleep(1)
    return True
    # except:
    #     return False

def detectWinOrLose():
    try:
        x, y= pyautogui.locateCenterOnScreen("pics/win.png")
        _betCounter = 1
        print("Gewonnen! Bet-Counter auf 1 gesetzt")
    except:
        try:
            x,y = pyautogui.locateCenterOnScreen("pics/lose.png")
            _betCounter*=2
            print("Verloren! Bet-Counter verdoppelt auf " + _betCounter)
        except:
            return False
    return True

def moveMouseTo(x, y):
    pyautogui.moveTo(100, 100, duration = 5)
    print("debug: mouse moved to ({x}, {y})")


if __name__ == "__main__":
    startup()

#maus auf rot -> max einsatz -> einsatz-counter abarbeiten (place orders)
#detection for win/lose -> einsatz-counter verdoppeln oder zurücksetzen

