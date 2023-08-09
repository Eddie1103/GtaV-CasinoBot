import requests
import pyautogui
import time, os
from screenSize import GetScreenSize
from directkeys import PressKey, ReleaseKey, TAB, UP
from screenshot import Screen
from pynput import mouse

_betCounter = 1
SCREEN_SIZE = GetScreenSize()
SCREEN_STRING = str(SCREEN_SIZE[0]) + "x" + str(SCREEN_SIZE[1])
OFFSET_SIZE = 90
API_URL = 'https://ocr.k0ntr4.de/extract_text'

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

def ratingApiReturn(value):
    global _betCounter
    value = value["text"]
    if "gewonnen" in value.lower() or "win" in value.lower():
        #hier zurücksetzen
        _betCounter = 1
        print("Gewonnen! Bet-Counter auf 1 gesetzt")
        return True
    elif "verloren" in value.lower() or "lose" in value.lower():
        _betCounter *= 2
        print("Verloren! Bet-Counter verdoppelt auf " + str(_betCounter))
        return True
    return False

def get_jetons_coords():
    view = None
    if SCREEN_SIZE == (1920, 1080):
        view = (700, 120, 1700, 900)
    elif SCREEN_SIZE == (2560, 1440):
        view = (850, 170, 2300, 1100)
    if view:
        coords = pyautogui.locateCenterOnScreen(f'pics/jetons{SCREEN_STRING}.png', confidence=0.8, region=view)
    else:
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
    global _betCounter
    try:
        coords = pyautogui.locateCenterOnScreen(f'pics/bet{SCREEN_STRING}.png', confidence=0.8)
        if coords == None:
            return False
        print("Tisch gefunden!")
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
            print(currentMousePos, coords, coordsJetons)

        #max einsatz
        #PressKey(TAB)
        #time.sleep(0.5)
        #ReleaseKey(TAB)

        #2->500 3->1000 4->5000 5->10000
        for i in range(3):
            PressKey(UP)
            time.sleep(0.05)
            ReleaseKey(UP)

        for i in range(_betCounter):
            mouse.Controller().press(mouse.Button.left)
            time.sleep(0.1)
            mouse.Controller().release(mouse.Button.left)
            time.sleep(0.5)
        return True
    except:
        return False

def detectWinOrLose():
    Screen().take_screenshot(40, 25, SCREEN_SIZE[0] / 3, 250)
    # Load the image file
    image_file = {'image': ('image.png', open('pics/img.png', 'rb'))}
    # Send the POST request
    response = requests.post(API_URL, files=image_file)
    print(response.json())
    return ratingApiReturn(response.json())

def moveMouseTo(x, y):
    pyautogui.moveTo(100, 100, duration = 5)
    print("debug: mouse moved to ({x}, {y})")


if __name__ == "__main__":
    startup()

#maus auf rot -> max einsatz -> einsatz-counter abarbeiten (place orders)
#detection for win/lose -> einsatz-counter verdoppeln oder zurücksetzen

