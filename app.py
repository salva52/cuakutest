from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura tu API key de OpenAI
openai.api_key = 'TU_API_KEY_DE_OPENAI'

@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    url = data['url']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])

    summary = openai.Completion.create(
        engine="davinci",
        prompt=f"Resume el siguiente texto:\n\n{text}",
        max_tokens=100
    )

    questions = openai.Completion.create(
        engine="davinci",
        prompt=f"Genera preguntas de opción múltiple basadas en el siguiente texto:\n\n{summary['choices'][0]['text']}",
        max_tokens=200
    )

    questions_list = questions['choices'][0]['text'].split('\n')
    return jsonify({'questions': [q for q in questions_list if q.strip()]})

if __name__ == '__main__':
    app.run(debug=True)
