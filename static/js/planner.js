document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("event-modal");
    const modalDate = document.getElementById("modal-date");
    const eventText = document.getElementById("event-text");
    const existingEvents = document.getElementById("existing-events");
    let selectedDate = null;

    // Open modal on day click
    document.querySelectorAll(".calendar-day").forEach(day => {
        day.addEventListener("click", () => {
            selectedDate = day.dataset.date;
            modalDate.textContent = selectedDate;
            eventText.value = "";
            
            existingEvents.innerHTML = ""; // clear
            const events = day.querySelectorAll(".events-list li");
            events.forEach((ev, index) => {
                const li = document.createElement("li");
                li.textContent = ev.textContent;

                const delBtn = document.createElement("button");
                delBtn.textContent = "Delete";
                delBtn.style.marginLeft = "10px";
                delBtn.classList.add("delete-btn");

                delBtn.addEventListener("click", () => {
                    fetch("/delete_event", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ date: selectedDate, index: index })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.success) location.reload();
                    });
                });

                li.appendChild(delBtn);
                existingEvents.appendChild(li);
            });

            modal.style.display = "block";
        });
    });

    // Close modal
    document.getElementById("close-modal").addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Save event
    document.getElementById("save-event-btn").addEventListener("click", () => {
        const text = eventText.value.trim();
        if (!text) return;

        fetch("/save_event", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ date: selectedDate, event: text })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) location.reload();
        });
    });
});
