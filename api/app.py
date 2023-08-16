from flask import Flask, request, jsonify, render_template
from rembg import remove
from PIL import Image
import io
import base64
from flask_cors import CORS  # Import the CORS module

app = Flask(__name__)
CORS(app)  # Add CORS middleware to the app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    print('Removing background')
    try:
        uploaded_image = base64.b64decode(request.data)
        # Decode base64 image data
        print("Decoded image data")

        input_image = Image.open(io.BytesIO(uploaded_image))  # Open image using PIL
        print("Image opened")

        output_image = remove(input_image)  # Perform background removal using rembg
        print("Background removed")

        buffered = io.BytesIO()
        output_image.save(buffered, format="PNG")  # Convert image to base64-encoded PNG
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return jsonify({"result": encoded_image}), 200
    except Exception as e:
        print("Failed:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
