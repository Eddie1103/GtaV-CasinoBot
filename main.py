import pyautogui
import time

_amount = 1000

def startup():
    print("Casino-Bot is starting...")
    moveMouseTo(100, 100)
    exit()


def moveMouseTo(x, y):
    pyautogui.moveTo(100, 100, duration = 5)
    print("debug: mouse moved to ({x}, {y})")


if __name__ == "__main__":
    startup()

#maus auf rot -> max einsatz -> einsatz-counter abarbeiten (place orders)
#detection for win/lose -> einsatz-counter verdoppeln oder zurücksetzen