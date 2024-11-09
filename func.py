import whisper
import os
from transformers import pipeline


model = whisper.load_model("base")
audio_file_path = os.path.expanduser("~/Downloads/gracesday.mp3")
result = model.transcribe(audio_file_path)
print(result["text"])


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

print(summarizer(result["text"], max_length=130, min_length=100, do_sample=False))
