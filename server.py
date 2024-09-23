from flask import Flask, request, jsonify
from flask_cors import CORS
from main import audio_to_text, get_response
import messages as m
app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.get_json()
    response = get_response(user_input['prompt'])
    return jsonify({'response': response})

@app.route('/speech', methods=['POST'])
def speech():
    if 'audio' not in request.files:
        return jsonify({'error': True})
    audio_file = request.files['audio']
    try:
        audio_file.save(m.homePath+m.audioFilePath+'/audio.webm')
        userContent = audio_to_text('audio.webm')
        if userContent == False:
            return jsonify({'error': True})
        botContent = get_response(userContent)
        return jsonify({'response': botContent, 'requestPrompt': userContent})

    except Exception as e:
        return jsonify({'error': True})

@app.route('/check', methods=['POST'])
def check():
    return jsonify({'messages': m.messagesExist(), 'audio': m.audioExist(), 'number': m.numberExist()})

@app.route('/createFiles', methods=['POST'])
def createFiles():
    filetype = request.get_json()
    try:
        if filetype['file'] == 'messages':
            m.createMessageFilePath()
            return jsonify({'bool': True})
        elif filetype['file'] == 'audio':
            m.createAudioFilePath()
            return jsonify({'bool': True})
        elif filetype['file'] == 'number':
            m.createNumberFilePath()
            return jsonify({'bool': True})
    except:
        return jsonify({'bool': False})

@app.route('/read', methods=['POST'])
def read():
    chatHistory = m.readFile()
    if (chatHistory==False):
        return jsonify({'json': False})
    else:
        return jsonify({'json': f'{chatHistory}'})
    
@app.route('/rean', methods=['POST'])
def rean():
    chatHistory = m.readNumberFile()
    if (chatHistory==False):
        return jsonify({'json': 'error'})
    else:
        return jsonify({'json': f'{chatHistory}'})
    
@app.route('/writn', methods=['POST'])
def writn():
    data = request.get_json()
    if m.writeNumber(data['number_of_messages']):
        return jsonify({'bool': True})
    else:
        return jsonify({'bool': False})
    
@app.route('/write', methods=['POST'])
def write():
    data = request.get_json()
    if m.write(data):
        return jsonify({'bool': True})
    else:
        return jsonify({'bool': False})

if __name__ == '__main__':
    app.run(debug=True)