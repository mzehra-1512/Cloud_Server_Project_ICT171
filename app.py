from datetime import date
from flask import Flask, render_template, request, jsonify
import json, os

#--Flask App Setup--
app = Flask(__name__)

#Path to notes data file
DATA_FILE = 'data/notes.json'
TODO_FILE = 'data/todo.json'
POMODORO_FILE = 'data/pomodoro.json'

os.makedirs('data', exist_ok=True)

if not os.path.exists(DATA_FILE):
     with open(DATA_FILE, 'w') as f:
          json.dump([], f)
if not os.path.exists(TODO_FILE):
    with open(TODO_FILE, 'w') as f:
        json.dump([], f)
if not os.path.exists(POMODORO_FILE):
    with open(POMODORO_FILE, 'w') as f:
        json.dump({"custom_time": 25}, f)


#--Helper Functions--
def load_notes():
     if not os.path.exists(DATA_FILE):
          return[]
     with open(DATA_FILE, "r") as file:
          try: 
               return json.load(file)
          except json.JSONDecodeError:
               return[]
          
def save_notes(notes):
     with open(DATA_FILE, "w") as file:
          json.dump(notes, file, indent =4)


#--Routes for pages-- 
@app.route('/')
def home_page(): 
    notes_list = load_notes()[::-1]
    todos = load_todos()
    today_str = date.today().strftime("%m/%d/%Y")
    todays_todo = next((t for t in todos if t["date"] == today_str), None)
    return render_template("home.html", notes=notes_list, todays_todo=todays_todo)

@app.route('/todo')
def todo_page(): 
    todos = load_todos()
    return render_template("todo.html", todos=todos)

@app.route('/notes')
def notes():
    notes_list = load_notes()
    return render_template('notes.html', notes=notes_list)

@app.route('/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')

#--API for saving notes--
@app.route('/save_note', methods=['POST'])
def save_note_route():
     data = request.get_json()
     notes = load_notes()
     new_note = {
          "content" : data["content"],
          "date" : data["date"]
     }
     notes.append(new_note)
     save_notes(notes)
     return jsonify({"message": "Note saved successfully!"})

@app.route('/delete_note', methods=['POST'])
def delete_note():
    data = request.get_json()
    note_date = data.get("date")
    notes = load_notes()
    notes = [note for note in notes if note["date"] != note_date]
    save_notes(notes)
    return jsonify({"message": "Note deleted successfully!"})

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)


@app.route('/save_todo', methods=['POST'])
def save_todo():
    data = request.get_json()
    data.setdefault("items", [])
    if not isinstance(data["items"], list):
        data["items"] = []
    todos = load_todos()
    todos.append(data)
    save_todos(todos)
    return jsonify({"message": "Todo list saved successfully!"})

@app.route('/delete_todo', methods=['POST'])
def delete_todo():
    data = request.get_json()
    todos = load_todos()
    todos = [t for t in todos if t["date"] != data["date"]]
    save_todos(todos)
    return jsonify({"message": "Todo list deleted successfully!"})

def load_pomodoro():
    if os.path.exists(POMODORO_FILE):
        with open(POMODORO_FILE, 'r') as f:
            return json.load(f)
    return {"custom_time": 25}

def save_pomodoro(data):
    with open(POMODORO_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/pomodoro')
def pomodoro():
    pomodoro_data = load_pomodoro()
    return render_template('pomodoro.html', custom_time=pomodoro_data.get("custom_time", 25))

@app.route('/save_pomodoro', methods=['POST'])
def save_pomodoro_route():
    data = request.get_json()
    save_pomodoro(data)
    return jsonify({"message": "Custom time saved!"})




#--Run the app--
if __name__== '__main__':
     app.run(debug=True)

    



	