let timer;
let totalSeconds;
let isRunning = false;
let customMinutes = 25;

function updateDisplay() {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    document.getElementById("time-display").textContent =
        `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // Animate circle
    const progress = (1 - totalSeconds / (customMinutes * 60)) * 360;
    document.querySelector(".timer-circle").style.background = 
        `conic-gradient(#15b2af ${progress}deg, #f0f0f0 ${progress}deg)`;
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    timer = setInterval(() => {
        if (totalSeconds > 0) {
            totalSeconds--;
            updateDisplay();
        } else {
            clearInterval(timer);
            isRunning = false;
            alert("Time’s up! Take a break ☕");
        }
    }, 1000);
}

function pauseTimer() {
    clearInterval(timer);
    isRunning = false;
}

function resetTimer() {
    clearInterval(timer);
    isRunning = false;
    totalSeconds = customMinutes * 60;
    updateDisplay();
}

function setCustomTime() {
    const minutes = parseInt(document.getElementById("minutesInput").value);
    if (minutes < 1 || minutes > 60) {
        document.getElementById("saveMessage").textContent = "Enter 1–60 minutes.";
        return;
    }

    customMinutes = minutes;
    totalSeconds = customMinutes * 60;
    updateDisplay();

    // Save to backend
    fetch("/save_pomodoro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ custom_time: minutes })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("saveMessage").textContent = data.message;
        setTimeout(() => document.getElementById("saveMessage").textContent = "", 2000);
    });
}

window.onload = function() {
    totalSeconds = {{ custom_time|default(25) }} * 60;
    customMinutes = {{ custom_time|default(25) }};
    updateDisplay();
};
