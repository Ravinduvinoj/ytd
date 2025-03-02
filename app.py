from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import re
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Ensure the 'downloads' directory exists
DOWNLOADS_DIR = os.path.join(os.getcwd(), 'downloads')
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

# Function to extract YouTube video ID from various URL formats
def extract_video_id(url):
    match = re.search(r"(?:v=|\/(?:embed|shorts|watch)\?v=|youtu\.be\/|\/v\/|\/e\/|watch\?v=|watch\?.+&v=)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "YouTube URL is required"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    output_path = os.path.join(DOWNLOADS_DIR, f"{video_id}.mp4")

    try:
        # Run yt-dlp to download the video
        subprocess.run(
            ["yt-dlp", "-f", "best", "-o", output_path, url],
            check=True,
            capture_output=True,
            text=True
        )

        # Check if file exists before sending
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({"error": "File not found after download"}), 404

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Download failed: {e.stderr}"}), 500

@app.route('/')
def home():
    return "YouTube Downloader API is running!"

if __name__ == '__main__':
    app.run(debug=True, port=3000)
