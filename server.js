const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const app = express();
const PORT = 3000;

// Enable CORS
app.use(cors());
app.use(express.json());

// Serve static files from 'downloads' folder for direct access if needed
app.use('/downloads', express.static(path.join(__dirname, 'downloads')));

app.post('/download', (req, res) => {
  const { url } = req.body;
  if (!url) {
    return res.status(400).json({ error: 'YouTube URL is required' });
  }

  const ytDlpPath = path.join(__dirname, 'yt-dlp.exe');
  const outputPathTemplate = path.join(__dirname, 'downloads', '%(id)s.%(ext)s'); // Use video ID to prevent naming issues

  const process = spawn(ytDlpPath, ['-f', 'best', '-o', outputPathTemplate, url]);

  process.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  process.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  process.on('close', (code) => {
    if (code === 0) {
      const videoFilePath = path.join(__dirname, 'downloads', `${url.match(/(?:v=)(.*?)(?:&|$)/)[1]}.mp4`);
      
      // Ensure the file exists before sending
      if (fs.existsSync(videoFilePath)) {
        const file = fs.createReadStream(videoFilePath);
        res.setHeader('Content-Disposition', `attachment; filename="${path.basename(videoFilePath)}"`);
        res.setHeader('Content-Type', 'video/mp4');
        file.pipe(res);
      } else {
        res.status(404).json({ error: 'File not found after download' });
      }
    } else {
      res.status(500).json({ error: 'Download failed' });
    }
  });
});


app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
