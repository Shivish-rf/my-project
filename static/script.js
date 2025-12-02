let questions = [];
let index = 0;
let score = 0;
let timer = 30;
let countdown;

let username = localStorage.getItem("username");
document.getElementById("username-display").innerText = "Player: " + username;

// Fetch questions from backend
fetch("/get_questions")
    .then(res => res.json())
    .then(data => {
        questions = data;
        showQuestion();
        startTimer();
    });

// Show question
function showQuestion() {
    document.getElementById("question").innerText = questions[index].question;
    let optionsDiv = document.getElementById("options");
    optionsDiv.innerHTML = "";

    questions[index].options.forEach(option => {
        let btn = document.createElement("button");
        btn.innerText = option;
        btn.onclick = () => checkAnswer(option);
        optionsDiv.appendChild(btn);
    });
}

// Check answer
function checkAnswer(selected) {
    if (selected === questions[index].answer) score++;
    nextQuestion();
}

// Timer logic
function startTimer() {
    countdown = setInterval(() => {
        timer--;
        document.getElementById("timer").innerText = "Time: " + timer;
        if (timer === 0) nextQuestion();
    }, 1000);
}

// Next question
function nextQuestion() {
    timer = 30;
    index++;
    if (index >= questions.length) return finishQuiz();
    showQuestion();
}

// Submit score when finished
function finishQuiz() {
    clearInterval(countdown);
    fetch("/submit_score", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: username, score: score})
    }).then(() => {
        window.location.href = "/leaderboard";
    });
}
