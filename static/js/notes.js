// --- Text Formatting Functions ---
function format(command, value = null) {
    document.getElementById('editor').focus();
    document.execCommand(command, false, value);
}

function setColor() {
    const color = document.getElementById('colorPicker').value;
    document.getElementById('editor').focus();
    document.execCommand('foreColor', false, color);
}

// --- Save Note to Flask Backend ---
async function saveNote() {
    const content = document.getElementById('editor').innerHTML.trim();
    if (content === "") {
        document.getElementById("saveMessage").textContent = "Cannot save empty note!";
        return;
    }

    const note = {
        content: content,
        date: new Date().toLocaleString()
    };

    try{
        const response = await fetch("/save_note",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(note)
        });
        const result = await response.json();
        document.getElementById("saveMessage").textContent = result.message;

        setTimeout(() => {
            document.getElementById("saveMessage").textContent = "";
            window.location.reload();
        }, 2000);

        document.getElementById('editor').innerHTML = "";
    } catch (error) {
        console.error("Error saving note:", error);
        document.getElementById("saveMessage").textContent = "Error saving note!";
    }
}

function downloadNote(content, date) {
    // Create a Blob from the note content
    const blob = new Blob([content], { type: "text/plain" });

    // Create a temporary link element
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);

    // Use date for the filename
    link.download = `note-${date.replace(/[/, :]/g, "-")}.txt`;

    // Trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function downloadNoteFromButton(btn) {
    let content = btn.getAttribute('data-content');

    // Create a temporary div to strip HTML tags
    const tempDiv = document.createElement("div");
    tempDiv.innerHTML = content;
    content = tempDiv.textContent || tempDiv.innerText || "";

    const date = btn.getAttribute('data-date');

    const blob = new Blob([content], { type: "text/plain" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = `note-${date.replace(/[/, :]/g, "-")}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

async function deleteNote(noteDate) {
    if (!confirm("Are you sure you want to delete this note?")) return;

    try {
        const response = await fetch("/delete_note", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ date: noteDate })
        });
        const result = await response.json();
        alert(result.message);
        window.location.reload();
    } catch (error) {
        console.error("Error deleting note:", error);
        alert("Error deleting note!");
    }
}
