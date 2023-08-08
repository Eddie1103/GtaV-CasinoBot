from PIL import ImageGrab

class Screen():
    def take_screenshot(self, x1, y1, x2, y2):
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img = img.convert('L')
        try:
            img.save("pics/img.png")
        except:
            return