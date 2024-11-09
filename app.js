const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");  // To execute the Python script
const path = require("path");
const fs = require("fs");
const app = express();
const PORT = 3000;

app.use(cors());

// Ensure the uploads folder exists
const uploadDir = "uploads/";
if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
}

// Set up multer for file handling
const upload = multer({ dest: "uploads/" });

// Endpoint to handle file upload and conversion
app.post("/upload", upload.single("audio"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: "No file uploaded" });
    }

    console.log(`File uploaded: ${req.file.path}`);

    const pythonFile = path.resolve("tts.py");  // Ensure the Python file path is correct
    const filePath = path.resolve(req.file.path);  // Resolve the absolute path for the uploaded file

    // Call the Python script and pass the file path as an argument
    const pythonProcess = exec(`python ${pythonFile} ${filePath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ message: "Error processing file", error: stderr });
        }

        // Send back the transcription result
        res.json({ message: "File processed successfully", text: stdout });
    });

    // If there's an error in the Python process
    pythonProcess.stderr.on("data", (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.stdout.on("data", (data) => {
        console.log(`stdout: ${data}`);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
