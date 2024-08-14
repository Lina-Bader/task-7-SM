from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from flask import Flask, render_template, request, jsonify
import pyttsx3
import openai
import speech_recognition as sr
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=text,
            max_tokens=150
        )
        response_text = response.choices[0].text.strip()
        return jsonify({'text': response_text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand audio'}), 400
    except sr.RequestError:
        return jsonify({'error': 'Could not request results'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    # Save the audio file
    audio_file_path = 'static/response.wav'
    engine.save_to_file(text, audio_file_path)
    engine.runAndWait()
    
    return jsonify({'audio_url': '/static/response.wav'})

if __name__ == '__main__':
    app.run(debug=True)

