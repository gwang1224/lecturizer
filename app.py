from flask import Flask, request, render_template, jsonify
import os
import whisper
from werkzeug.utils import secure_filename
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Set up the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'flac', 'webm'}  # Add 'webm'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part in the request")  # Debugging statement
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print("File received:", file.filename)  # Debugging statement

    if file.filename == '':
        print("No selected file")  # Debugging statement
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print("File saved at:", filepath)  # Debugging statement

        # Run transcription and summarization
        result_text = run_func(filepath)
        print("Transcription and summarization complete.")  # Debugging statement
        return jsonify({'summary': result_text})

    print("File type not allowed")  # Debugging statement
    return jsonify({'error': 'File type not allowed'}), 400

def run_func(audio_file_path):
    print("Transcribing audio...")  # Debugging statement
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    transcribed_text = result["text"]
    print("Transcription complete:", transcribed_text[:100])  # Log first 100 chars of transcript

    print("Summarizing text...")  # Debugging statement
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(transcribed_text, max_length=130, min_length=5, do_sample=False)
    print("Summary complete:", summary[0]['summary_text'])  # Debugging statement

    return summary[0]['summary_text']

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
