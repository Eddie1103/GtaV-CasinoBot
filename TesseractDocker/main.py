from PIL import Image, ImageGrab
import pytesseract as pt
from flask import Flask, request, jsonify

pt.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update this path

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    # Retrieve the image file from the request
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    # Process the image
    img = Image.open(image_file)
    img_txt = pt.image_to_string(img)

    return jsonify({"text": img_txt})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

