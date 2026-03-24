
import os
from flask import Flask, render_template, request, jsonify, send_file
from empathy_engine import EmpathyEngine

app = Flask(__name__)
engine = EmpathyEngine(use_offline=False)  # Use gTTS for web (better quality)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Generate speech
        audio_file = engine.generate_speech(text)
        
        # Return audio file path
        return jsonify({
            'success': True,
            'audio_file': audio_file,
            'emotion': engine.detect_emotion(text)[0]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/audio/<filename>')
def get_audio(filename):
   
    return send_file(filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True, port=5000)