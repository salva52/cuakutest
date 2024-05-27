from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='', static_url_path='')
CORS(app)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    url = data['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])

    # Usar la nueva API de OpenAI para resumir el texto
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Resume el siguiente texto:\n\n{text}",
        max_tokens=100
    )
    summary = response.choices[0].text.strip()

    # Usar la nueva API de OpenAI para generar preguntas
    response = client.completions.create(
        model="text-davinci-003",
        prompt=f"Genera preguntas de opción múltiple basadas en el siguiente texto:\n\n{summary}",
        max_tokens=200
    )
    questions = response.choices[0].text.strip().split('\n')

    return jsonify({'questions': [q for q in questions if q.strip()]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
