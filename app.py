from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Endpoint to summarize text
@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.json
    transcript = data.get('text', '')

    # Generate summary
    summary = summarizer(transcript, max_length=130, min_length=100, do_sample=False)
    summarized_text = summary[0]['summary_text']

    # Return the summary as JSON
    return jsonify({'summary': summarized_text})

if __name__ == '__main__':
    app.run(port=5000)
