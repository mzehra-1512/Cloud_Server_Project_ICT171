from datetime import date
from flask import Flask, render_template, request, jsonify
import json, os
import calendar

#--Flask App Setup--
app = Flask(__name__)

#Path to notes data file
DATA_FILE = 'data/notes.json'
TODO_FILE = 'data/todo.json'
POMODORO_FILE = 'data/pomodoro.json'
PLANNER_FILE = 'data/planner.json'

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
if not os.path.exists(PLANNER_FILE):
    with open(PLANNER_FILE, 'w') as f:
        json.dump({}, f)

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

def load_planner():
    if os.path.exists(PLANNER_FILE):
        with open(PLANNER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_planner(planner_data):
    with open(PLANNER_FILE, 'w') as f:
        json.dump(planner_data, f, indent=4)


# Planner page route
@app.route('/planner')
def planner():
    year = request.args.get('year', date.today().year, type=int)
    month = request.args.get('month', date.today().month, type=int)
    cal = calendar.Calendar(firstweekday=0)
    month_days = cal.monthdayscalendar(year, month)  # list of weeks
    planner_data = load_planner()
    month_name = calendar.month_name[month]  # Get full month name
    return render_template('planner.html', month_days=month_days, year=year, month=month, month_name=month_name, planner_data=planner_data)

# API to save events
@app.route('/save_event', methods=['POST'])
def save_event():
    data = request.get_json()
    date_str = data.get("date")  # format: YYYY-MM-DD
    event_text = data.get("event", "").strip()
    if not date_str or not event_text:
        return jsonify({"success": False, "message": "Invalid data"}), 400

    planner_data = load_planner()
    if date_str not in planner_data:
        planner_data[date_str] = []
    planner_data[date_str].append(event_text)
    save_planner(planner_data)
    return jsonify({"success": True, "message": "Event saved!"})


# API to delete event
@app.route('/delete_event', methods=['POST'])
def delete_event():
    data = request.get_json()
    date_str = data.get("date")
    index = data.get("index")
    planner_data = load_planner()
    if date_str in planner_data and 0 <= index < len(planner_data[date_str]):
        planner_data[date_str].pop(index)
        if not planner_data[date_str]:
            del planner_data[date_str]
        save_planner(planner_data)
        return jsonify({"success": True})
    return jsonify({"success": False}), 400


#--Run the app--
if __name__== '__main__':
     app.run(debug=True)

