document.addEventListener("DOMContentLoaded", () => {
    const circle = document.querySelector(".timer-circle");
    let customMinutes = parseInt(circle.dataset.customTime) || 25;
    let totalSeconds = customMinutes * 60;
    let timer = null;
    let isRunning = false;

    const display = document.getElementById("time-display");
    const startBtn = document.getElementById("start-btn");
    const pauseBtn = document.getElementById("pause-btn");
    const resetBtn = document.getElementById("reset-btn");
    const saveBtn = document.getElementById("save-time-btn");
    const timeInput = document.getElementById("minutesInput");

    // Functions
    function updateDisplay() {
        const minutes = Math.floor(totalSeconds / 60);
        const seconds = totalSeconds % 60;
        display.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

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
                alert("Time’s up! Take a break ");
                startBtn.classList.remove("active");
            }
        }, 1000);

        startBtn.classList.add("active");
        pauseBtn.classList.remove("active");
    }


    function pauseTimer() {
        clearInterval(timer);
        isRunning = false;

        pauseBtn.classList.add("active");
        startBtn.classList.remove("active");
    }

    function resetTimer() {
        clearInterval(timer);
        isRunning = false;
        totalSeconds = customMinutes * 60;
        updateDisplay();

        startBtn.classList.remove("active");
        pauseBtn.classList.remove("active");

    }

    function setCustomTime() {
        const minutes = parseInt(timeInput.value);
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

    // Attach event listeners
    startBtn.addEventListener("click", startTimer);
    pauseBtn.addEventListener("click", pauseTimer);
    resetBtn.addEventListener("click", resetTimer);
    saveBtn.addEventListener("click", setCustomTime);

    // Initialize display
    updateDisplay();

});
