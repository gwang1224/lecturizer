from flask import Flask, request, render_template, jsonify
import os
import whisper
from werkzeug.utils import secure_filename
from transformers import pipeline

app = Flask(__name__)

# Set up the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'mp3', 'wav', 'ogg', 'flac'}  # Add other audio formats as needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Run transcription and summarization
        result_text = run_func(filepath)
        return jsonify({'summary': result_text})

    return jsonify({'error': 'File type not allowed'}), 400

def run_func(audio_file_path):
    # Load the whisper model and transcribe the audio
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    transcribed_text = result["text"]

    # Summarize the transcribed text
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(transcribed_text, max_length=130, min_length=100, do_sample=False)

    return summary[0]['summary_text']

if __name__ == '__main__':
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
