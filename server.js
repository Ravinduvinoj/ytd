const express = require("express");
const cors = require("cors");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3000;

// Enable CORS
app.use(cors());
app.use(express.json());

// Create downloads directory if it doesn't exist
const downloadsDir = path.join(__dirname, "downloads");
if (!fs.existsSync(downloadsDir)) {
    fs.mkdirSync(downloadsDir, { recursive: true });
}

// Serve static files from 'downloads' folder for direct access if needed
app.use("/downloads", express.static(downloadsDir));

app.post("/download", (req, res) => {
    const { url } = req.body;
    if (!url) {
        return res.status(400).json({ error: "YouTube URL is required" });
    }

    // Use yt-dlp (Python package) instead of yt-dlp.exe
    const outputPathTemplate = path.join(downloadsDir, "%(id)s.%(ext)s"); // Use video ID to prevent naming issues

    const process = spawn("yt-dlp", ["-f", "best", "-o", outputPathTemplate, url]);

    process.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
    });

    process.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
    });

    process.on("close", (code) => {
        if (code === 0) {
            // Extract the video ID from the URL
            const videoIdMatch = url.match(/(?:v=|youtu\.be\/)([\w-]+)/);
            if (!videoIdMatch) {
                return res.status(500).json({ error: "Invalid YouTube URL format" });
            }

            const videoFilePath = path.join(downloadsDir, `${videoIdMatch[1]}.mp4`);

            // Ensure the file exists before sending
            if (fs.existsSync(videoFilePath)) {
                res.download(videoFilePath, path.basename(videoFilePath));
            } else {
                res.status(404).json({ error: "File not found after download" });
            }
        } else {
            res.status(500).json({ error: "Download failed" });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
