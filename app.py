from flask import Flask, request, jsonify, render_template
import os
from utils.file_reader import read_file
from utils.summarizer import summarize
from utils.chatbot import chat_with_data

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global variables
current_data = None
current_data_type = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_data, current_data_type

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded!'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected!'})

    # File save karo
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # File read karo
    current_data, current_data_type = read_file(filepath)

    if current_data_type == 'unsupported':
        return jsonify({'error': 'Unsupported file type!'})

    # Summary banao
    summary = summarize(current_data, current_data_type)

    return jsonify({
        'success': True,
        'summary': summary,
        'data_type': current_data_type
    })

@app.route('/chat', methods=['POST'])
def chat():
    global current_data, current_data_type

    if current_data is None:
        return jsonify({'error': 'Pehle file upload karo!'})

    user_message = request.json.get('message', '')

    if not user_message:
        return jsonify({'error': 'Message khali hai!'})

    # AI se jawab lo
    response = chat_with_data(user_message, current_data, current_data_type)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)