
let startTime;

function startTest() {
    startTime = new Date().getTime();
}

function submitTest() {
    let endTime = new Date().getTime();
    let timeSpent = (endTime - startTime) / 1000;
    let correct = document.querySelector('input[name="answer"]:checked').value == "4" ? 1 : 0;
    let attempts = 1; // Could be improved to track changes

    fetch('/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ correct, time_spent: timeSpent, attempts })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("result").innerText = "Suggested Difficulty for Test 2: " + data.suggested_difficulty;
    });
}
