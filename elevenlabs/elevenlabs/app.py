from flask import Flask, request, render_template, url_for
import requests
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    text = request.form['text']
    url = "https://api.elevenlabs.io/v1/text-to-speech/9WzjwSO57V4Sd9i7pw08"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "d60710c75be53a564a2e1aa7b6686b28"
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=data, headers=headers)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Constrói o caminho absoluto para o arquivo
    filename = os.path.join(app.root_path, 'static', f'output_{timestamp}.mp3')
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                
    audio_url = url_for('static', filename=f'output_{timestamp}.mp3')
    return render_template('index.html', audio_url=audio_url)

if __name__ == '__main__':
    app.run(debug=True)