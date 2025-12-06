# audio-service/app.py
from flask import Flask, request, jsonify
import os, subprocess, uuid
import boto3

UPLOAD_FOLDER = "/data/videos"
OUT_FOLDER = "/data/audio"
os.makedirs(OUT_FOLDER, exist_ok=True)

S3_BUCKET = os.environ.get("S3_BUCKET", "")
REGION = os.environ.get("AWS_DEFAULT_REGION", "ap-south-1")

# boto3 client uses environment credentials configured in the pod (here using host creds)
s3 = boto3.client("s3", region_name=REGION)

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_audio():
    data = request.get_json(silent=True)
    if not data or "video_path" not in data:
        return jsonify({"error": "missing video_path"}), 400
    video_path = data["video_path"]
    if not os.path.exists(video_path):
        return jsonify({"error": "video not found", "path": video_path}), 404

    base = os.path.basename(video_path)
    name = os.path.splitext(base)[0]
    out_file = os.path.join(OUT_FOLDER, f"{name}.mp3")

    cmd = ["ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-q:a", "2", out_file]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "ffmpeg failed", "details": e.stderr.decode()[:1000]}), 500

    if S3_BUCKET:
        key = f"audio/{uuid.uuid4().hex}/{os.path.basename(out_file)}"
        try:
            s3.upload_file(out_file, S3_BUCKET, key)
            s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
            return jsonify({"s3_url": s3_url, "local_path": out_file})
        except Exception as e:
            return jsonify({"error": "s3 upload failed", "details": str(e)}), 500
    else:
        return jsonify({"local_path": out_file})

@app.route("/", methods=["GET"])
def home():
    return "Audio service running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
