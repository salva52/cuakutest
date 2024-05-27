document.getElementById('generateButton').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value;
    fetch('http://127.0.0.1:5000/generate-quiz', { // Asegúrate de que la URL esté correcta
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
    })
    .then(response => response.json())
    .then(data => {
        const quizContainer = document.getElementById('quizContainer');
        quizContainer.innerHTML = '';
        data.questions.forEach((question, index) => {
            const questionElement = document.createElement('div');
            questionElement.innerHTML = `<p>${index + 1}. ${question}</p>`;
            quizContainer.appendChild(questionElement);
        });
    })
    .catch(error => console.error('Error:', error));
});
