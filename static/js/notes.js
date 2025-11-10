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