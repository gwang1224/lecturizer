const express = require("express");
const multer = require("multer");
const cors = require("cors");
const { exec } = require("child_process");  // To execute the Python script
const app = express();
const PORT = 3000;

app.use(cors());

// Set up multer for file handling
const upload = multer({ dest: "uploads/" });

// Endpoint to handle file upload and conversion
app.post("/upload", upload.single("audio"), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: "No file uploaded" });
    }

    // The name of the Python file (make sure it's in the same directory as your Node.js file or specify the full path)
    const pythonFile = "tts.py"; 

    // Path to the uploaded file
    const filePath = req.file.path;

    // Call the Python script and pass the file path as an argument
    const pythonProcess = exec(`python3 ${pythonFile} ${filePath}`, (error, stdout, stderr) => {
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
});  // <-- This closes the post route function here

// Start the server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});  // <-- This closes the app.listen function here
