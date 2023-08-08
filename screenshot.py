from PIL import Image, ImageGrab
import pytesseract as pt

pt.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Screen():
    def take_screenshot(self, x1, y1, x2, y2):
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        img = img.convert('L')
        try:
            img.save("pics/img.png")
        except:
            return

    def get_text(self, x1, y1, x2, y2):
        self.take_screenshot(x1, y1, x2, y2)
        img = Image.open("pics/img.png")
        img_txt = ((pt.image_to_string(img)).encode("ascii", "ignore")).decode("utf-8")

        return img_txt

    def get_pixel_color(self, x1, y1, x2, y2, pixel_x, pixel_y):
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        image = image.convert('RGB')
        color = image.getpixel((pixel_x, pixel_y))
        return color