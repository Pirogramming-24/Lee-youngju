let attempts = 9;
let answer = [];

function initGame() {
    attempts = 9;
    answer = generateRandomNumbers();

    document.getElementById('attempts').textContent = attempts;

    document.getElementById('number1').value = '';
    document.getElementById('number2').value = '';
    document.getElementById('number3').value = '';

    document.getElementById('results').innerHTML = '';

    document.getElementById('game-result-img').src = '';

    document.querySelector('.submit-button').disabled = false;

    document.getElementById('number1').focus();

    console.log('정답:', answer);
}

function generateRandomNumbers() {
    const numbers = [];
    while (numbers.length < 3) {
        const randomNum = Math.floor(Math.random() * 10);
        if (!numbers.includes(randomNum)) {
            numbers.push(randomNum);
        }
    }
    return numbers;
}

function check_numbers() {
    const input1 = document.getElementById('number1').value;
    const input2 = document.getElementById('number2').value;
    const input3 = document.getElementById('number3').value;

    if (input1 === '' || input2 === '' || input3 === '') {
        document.getElementById('number1').value = '';
        document.getElementById('number2').value = '';
        document.getElementById('number3').value = '';
        document.getElementById('number1').focus();
        return;
    }

    const userInput = [
        parseInt(input1),
        parseInt(input2),
        parseInt(input3)
    ];

    let strike = 0;
    let ball = 0;

    for (let i = 0; i < 3; i++) {
        if (userInput[i] === answer[i]) {
            strike++;
        } else if (answer.includes(userInput[i])) {
            ball++;
        }
    }

    const resultsDiv = document.getElementById('results');
    const resultLine = document.createElement('div');
    resultLine.className = 'check-result';

    const leftDiv = document.createElement('div');
    leftDiv.className = 'left';
    leftDiv.textContent = userInput.join(' ');

    const colonDiv = document.createElement('div');
    colonDiv.textContent = ':';

    const rightDiv = document.createElement('div');
    rightDiv.className = 'right';

    if (strike === 0 && ball === 0) {
        const outSpan = document.createElement('span');
        outSpan.className = 'num-result out';
        outSpan.textContent = 'O';
        rightDiv.appendChild(outSpan);
    } else {
        if (strike > 0) {
            const strikeSpan = document.createElement('span');
            strikeSpan.className = 'num-result strike';
            strikeSpan.textContent = `${strike} S`;
            rightDiv.appendChild(strikeSpan);
            rightDiv.appendChild(document.createTextNode(' '));
        }
        if (ball > 0) {
            const ballSpan = document.createElement('span');
            ballSpan.className = 'num-result ball';
            ballSpan.textContent = `${ball} B`;
            rightDiv.appendChild(ballSpan);
        }
    }

    resultLine.appendChild(leftDiv);
    resultLine.appendChild(colonDiv);
    resultLine.appendChild(rightDiv);
    resultsDiv.appendChild(resultLine);

    document.getElementById('number1').value = '';
    document.getElementById('number2').value = '';
    document.getElementById('number3').value = '';
    document.getElementById('number1').focus();

    attempts--;
    document.getElementById('attempts').textContent = attempts;

    if (strike === 3) {
        endGame(true);
    } else if (attempts === 0) {
        endGame(false);
    }
}

function endGame(isWin) {
    const imgElement = document.getElementById('game-result-img');
    const submitButton = document.querySelector('.submit-button');

    if (isWin) {
        imgElement.src = './success.png';
    } else {
        imgElement.src = './fail.png';
    }

    submitButton.disabled = true;
}

window.addEventListener('DOMContentLoaded', () => {
    initGame();

    const inputs = document.querySelectorAll('.input-field');
    inputs.forEach((input, index) => {
        input.addEventListener('input', (e) => {
            if (e.target.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && e.target.value === '' && index > 0) {
                inputs[index - 1].focus();
            }

            if (e.key === 'Enter') {
                check_numbers();
            }
        });
    });
});
