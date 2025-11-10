let todoItems = [];

function addItem() {
    const input = document.getElementById('todoItemInput');
    const value = input.value.trim();
    if (!value) return;

    todoItems.push(value);

    const li = document.createElement('li');
    li.textContent = value;
    document.getElementById('todoItemList').appendChild(li);

    input.value = '';
}

async function saveTodo() {
    if (todoItems.length === 0) {
        document.getElementById('saveMessage').textContent = "Add at least one item!";
        return;
    }

    const todo = {
        items: todoItems,
        date: new Date().toLocaleDateString("en-US")
    };

    try {
        const response = await fetch('/save_todo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(todo)
        });

        const result = await response.json();
        document.getElementById('saveMessage').textContent = result.message;

        setTimeout(() => {
            document.getElementById('saveMessage').textContent = '';
            window.location.reload();
        }, 1500);

    } catch (error) {
        console.error("Error saving todo:", error);
        document.getElementById('saveMessage').textContent = "Error saving todo!";
    }
}

async function deleteTodo(date) {
    try {
        const response = await fetch('/delete_todo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ date })
        });

        const result = await response.json();
        window.location.reload();
    } catch (error) {
        console.error("Error deleting todo:", error);
    }
}
