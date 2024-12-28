import os
import io
from flask import Flask, request, jsonify
from config import Config

app = Flask(__name__)

import google.generativeai as genai

config = Config()
genai.configure(api_key=config.google_api_key)

from persona import Persona
from knowledge_base import KnowledgeBase

model = genai.GenerativeModel('gemini-pro')
default_persona = Persona(persona_file=config.default_persona_file)
default_knowledge = KnowledgeBase(knowledge_file=config.default_knowledge_file)

@app.route('/', methods=['GET'])
def index():
    return "MoChat API is running"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    persona_prompt = default_persona.get_persona_prompt()
    relevant_knowledge = default_knowledge.get_relevant_knowledge(message)
    prompt = persona_prompt + relevant_knowledge + message
    
    try:
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat_with_image', methods=['POST'])
def chat_with_image():
    data = request.form
    message = data.get('message')
    image = request.files.get('image')

    if not message or not image:
        return jsonify({'error': 'Message and image are required'}), 400
    
    # Image processing and Gemini API call
    try:
        from PIL import Image
        image_bytes = image.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        prompt = f"User message: {message}"
        response = model.generate_content([prompt, img])
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=config.port)

@app.route('/chat_with_voice', methods=['POST'])
def chat_with_voice():
    audio = request.files.get('audio')
    if not audio:
        return jsonify({'error': 'Audio file is required'}), 400
    
    # Audio processing and Gemini API call
    try:
        from google.cloud import speech
        import os
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = config.speech_credentials_file
        client = speech.SpeechClient()
        audio_bytes = audio.read()
        audio_content = speech.RecognitionAudio(content=audio_bytes)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
        )
        response = client.recognize(config=config, audio=audio_content)
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            prompt = f"User said: {transcript}"
            response = model.generate_content(prompt)
            return jsonify({'response': response.text})
        else:
            return jsonify({'error': 'Could not transcribe audio'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500