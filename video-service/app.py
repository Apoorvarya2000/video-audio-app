# video-service/app.py
from flask import Flask, request, jsonify
import os
import requests

UPLOAD_FOLDER = "/data/videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# audio-service DNS inside k8s
AUDIO_SERVICE = "http://audio-service:5001/extract"

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_videos():
    if "file" not in request.files:
        return jsonify({"error":"no file part"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error":"empty filename"}), 400
    filepath = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(filepath)
    try:
        r = requests.post(AUDIO_SERVICE, json={"video_path": filepath}, timeout=120)
        r.raise_for_status()
        return jsonify({"video_path": filepath, "audio_response": r.json()})
    except Exception as e:
        return jsonify({"error": "failed to call audio service", "details": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Video service running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
