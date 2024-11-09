from flask import Flask, request, render_template_string, redirect, url_for
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_OPENAI_API_KEY_PLS")

app = Flask(__name__)

# HTML content for index page
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Audio Summarizer</title>
</head>
<body>
    <h1>Upload an audio file to get a summary</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="audio_file" accept="audio/*" required>
        <input type="submit" value="Upload">
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(index_html)

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio_file' not in request.files:
        return redirect(url_for('index'))
    
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return redirect(url_for('index'))

    # Save the uploaded audio file
    audio_path = os.path.join("uploads", audio_file.filename)
    audio_file.save(audio_path)

    # Transcribe audio using Whisper API
    with open(audio_path, "rb") as audio:
        transcription = client.audio.transcriptions.create(model="whisper-1", file=audio)
    transcribed_text = transcription.text

    # Summarize transcription using GPT-4
    summary = summarize_text(transcribed_text)

    # Clean up by removing the uploaded audio file
    os.remove(audio_path)

    return f"<h1>Summary:</h1><p>{summary}</p><a href='/'>&larr; Go Back</a>"

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes transcriptions."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5000)