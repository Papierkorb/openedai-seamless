from io import BytesIO

from transformers import AutoProcessor, SeamlessM4Tv2Model
import torch
from flask import Flask, request, send_file
import soundfile as sf

app = Flask(__name__)

# Initialize the model
device = "cuda:0" if torch.cuda.is_available() else "cpu"
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large").to(device)

def synthesize_speech(text, language):
    text_inputs = processor(text=text, src_lang=language, return_tensors="pt").to(device)
    audio_array_from_text = model.generate(**text_inputs, tgt_lang=language)[0].cpu().numpy().squeeze()
    return audio_array_from_text

def convert_audio(audio_array, format, sample_rate):
    bytes = BytesIO()

    if format == "mp3":
        sf.write(bytes, audio_array, sample_rate, format='MP3', subtype='MPEG_LAYER_III')
    elif format == "flac":
        sf.write(bytes, audio_array, sample_rate, format='FLAC', subtype='PCM_16')
    elif format == "wav":
        sf.write(bytes, audio_array, sample_rate, format='WAV', subtype='PCM_16')
    
    return bytes

@app.route('/v1/audio/speech', methods=['POST'])
def speech():
    data = request.get_json()
    if 'input' not in data or 'language' not in data:
        return 'Missing required parameters', 400

    text = data['input']
    language = data['language']

    format = data.get('response_format', 'mp3')
    if format not in ['mp3', 'flac', 'wav']:
        return 'Unsupported format', 400

    audio_array = synthesize_speech(text, language)
    audio_io = convert_audio(audio_array, format, model.config.sampling_rate)
    audio_io.seek(0)
    return send_file(audio_io, mimetype=f'audio/{format}')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
