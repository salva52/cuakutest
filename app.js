document.getElementById('generateButton').addEventListener('click', () => {
    const url = document.getElementById('urlInput').value;
    fetch('/generate-quiz', { // La URL coincide con la ruta definida en Flask
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
