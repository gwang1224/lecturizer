// upload.js (Frontend JavaScript)

document.getElementById("audioUploadForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById("audioFile");
    const formData = new FormData();
    formData.append("audio", fileInput.files[0]);

    try {
        const response = await fetch("http://localhost:3000/upload", {
            method: "POST",
            body: formData
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to upload file");
    }
});
