from flask import Flask, render_template, request, jsonify
import json, os

#--Flask App Setup--
app = Flask(__name__)

#Path to notes data file
DATA_FILE = 'data/notes.json'

os.makedirs('data', exist_ok=True)

if not os.path.exists(DATA_FILE):
     with open(DATA_FILE, 'w') as f:
          json.dump([], f)



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
def home():
    notes_list = load_notes()
    notes_list = notes_list[::-1]
    return render_template('home.html', notes=notes_list)

@app.route('/notes')
def notes():
    notes_list = load_notes()
    return render_template('notes.html', notes=notes_list)

@app.route('/todo')
def todo():
    return render_template('todo.html')

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
#--Run the app--
if __name__== '__main__':
     app.run(debug=True)

    



	