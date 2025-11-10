from flask import Flask, render_template, request, jsonify
import json, os

#--Flask App Setup--
app = Flask(__name__)

#Path to notes data file
DATA_PATH = os.path.join("data", "notes.json")

#--Helper Functions--
def load_notes():
     if not os.path.exists(DATA_PATH):
          return[]
     with open(DATA_PATH, "r") as file:
          try: 
               return json.load(file)
          except json.JSONDecodeError:
               return[]
          
def save_notes(notes):
     with open(DATA_PATH, "w") as file:
          json.dump(notes, file, indent =4)


#--Routes for pages-- 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/notes')
def notes():
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
def save_notes():
     data = request.get_json()
     notes = load_notes()
     new_note = {
          "content" : data["content"],
          "date" : data["date"]
     }
     notes.append(new_note)
     save_note(notes)
     return jsonify({"message": "Note saved successfully!"})
#--Run the app--
if __name__== '__main__':
     os.makedirs("data", exist_ok=True)
     if not os.path.exists(DATA_PATH):
          save_notes([])
     app.run(debug=True)

    

	