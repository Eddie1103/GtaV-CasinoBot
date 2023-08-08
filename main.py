import pyautogui
import time, os
from screenSize import GetScreenSize
from directkeys import PressKey, ReleaseKey, TAB
from pynput import mouse

_betCounter = 1
SCREEN_SIZE = GetScreenSize()
SCREEN_STRING = str(SCREEN_SIZE[0]) + "x" + str(SCREEN_SIZE[1])
OFFSET_SIZE = 90

def startup():
    if os.path.exists("pics/bet" + SCREEN_STRING + ".png") == False:
        print("Kein Referenzbild für aktuelle Screen-Size gefunden: " + SCREEN_STRING +"px")
        exit()
    print("Casino-Bot is starting...")

    while(True):
        while(findBetField() == False):
            print("Konnte Tisch nicht finden...")
            time.sleep(5)
        exit()
        while(detectWinOrLose() == False):
            print("Runde läuft momentan...")
            time.sleep(2)

def get_jetons_coords():
    coords = pyautogui.locateCenterOnScreen(f'pics/jetons{SCREEN_STRING}.png', confidence=0.8)
    return coords

def get_bet_coords():
    coords = pyautogui.locateCenterOnScreen(f'pics/bet{SCREEN_STRING}.png', confidence=0.8)
    return coords

def check_if_coords_match_with_offset(coordsJetons, coordsBet, offset):
    if coordsJetons == None:
        return False
    elif coordsBet == None:
        return True
    return coordsJetons[0] + offset > coordsBet[0] and coordsJetons[0] - offset < coordsBet[0] and coordsJetons[1] + offset > coordsBet[1] and coordsJetons[1] - offset < coordsBet[1]

def get_direction_coords(coordsJetons, coords):
    offset = [0, 0]
    if coordsJetons[0] < coords[0]:
        offset[0] = OFFSET_SIZE
    elif coordsJetons[0] > coords[0]:
        offset[0] = -OFFSET_SIZE
    else:
        offset = 0
    if (coordsJetons[1] < coords[1]):
        offset[1] = OFFSET_SIZE
    elif coordsJetons[1] > coords[1]:
        offset[1] = -OFFSET_SIZE
    else:
        offset[1] = 0
    return offset

def findBetField():
    try:
        coords = pyautogui.locateCenterOnScreen(f'pics/bet{SCREEN_STRING}.png', confidence=0.8)
        if coords == None:
            return False
        coordsJetons = get_jetons_coords()
        while not check_if_coords_match_with_offset(coordsJetons, coords, 30):
            offset = get_direction_coords(coordsJetons, coords)
            currentMousePos = pyautogui.position()
            pyautogui.moveTo(currentMousePos[0] + offset[0], currentMousePos[1] + offset[1])
            if get_bet_coords() != None:
                coords = get_bet_coords()
            coordsJetons = get_jetons_coords()
            if coordsJetons == None:
                return False
        PressKey(TAB)
        time.sleep(0.5)
        ReleaseKey(TAB)
        for i in range(_betCounter):
            mouse.Controller().press(mouse.Button.left)
            time.sleep(0.1)
            mouse.Controller().release(mouse.Button.left)
            time.sleep(0.5)
        return True
    except:
        return False

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

