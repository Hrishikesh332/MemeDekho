from flask import Flask, request, jsonify
from flask_cors import CORS  
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
CORS(app) 

API_URL = os.getenv("API_URL")
HEADERS = {"Authorization": os.getenv("HF_AUTH_TOKEN")}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=HEADERS, data=data)
    return response.json()

@app.route("/upload", methods=["GET"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    if image.filename == "":
        return jsonify({"error": "No image selected"}), 400

    image_path = os.path.join("uploads", image.filename)
    image.save(image_path)
    result = query(image_path)
    os.remove(image_path)
    return jsonify(result)

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
