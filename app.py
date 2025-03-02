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
    print(f"Extracting video ID from URL: {url}")  # Debug print
    match = re.search(r"(?:v=|\/(?:embed|shorts|watch)\?v=|youtu\.be\/|\/v\/|\/e\/|watch\?v=|watch\?.+&v=)([a-zA-Z0-9_-]{11})", url)
    if match:
        video_id = match.group(1)
        print(f"Extracted video ID: {video_id}")  # Debug print
        return video_id
    print("No video ID found in URL")  # Debug print
    return None

@app.route('/download', methods=['POST'])

@app.before_request
def log_request_info():
    print(f"Request headers: {request.headers}")
    print(f"Request body: {request.get_json()}")
    print(f"X-Forwarded-For: {request.headers.get('X-Forwarded-For')}")
    print(f"Cloudfront-TLS: {request.headers.get('Cloudfront-Viewer-Tls')}")
    print(f"Access-Control-Request-Headers: {request.headers.get('Access-Control-Request-Headers')}")


def download_video():
    data = request.get_json()
    print(f"Received data: {data}")  # Debug print
    url = data.get('url')

    if not url:
        print("YouTube URL not provided")  # Debug print
        return jsonify({"error": "YouTube URL is required"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL")  # Debug print
        return jsonify({"error": "Invalid YouTube URL"}), 400

    output_path = os.path.join(DOWNLOADS_DIR, f"{video_id}.mp4")
    print(f"Output path for video: {output_path}")  # Debug print

    try:
        # Run yt-dlp to download the video
        print(f"Running yt-dlp for URL: {url}")  # Debug print
        result = subprocess.run(
            ["yt-dlp", "-f", "best", "-o", output_path, url],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"yt-dlp output: {result.stdout}")  # Debug print

        # Check if file exists before sending
        if os.path.exists(output_path):
            print(f"File found at {output_path}. Sending file.")  # Debug print
            return send_file(output_path, as_attachment=True)
        else:
            print("File not found after download")  # Debug print
            return jsonify({"error": "File not found after download"}), 404

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during download: {e.stderr}")  # Debug print
        return jsonify({"error": f"Download failed: {e.stderr}"}), 500

@app.route('/')
def home():
    return "YouTube Downloader API is running!"

if __name__ == '__main__':
    app.run(debug=True, port=3000)
