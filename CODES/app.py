from flask import Flask, render_template

#--Flask App Setup--
app = Flask(_name_)

#--Routes for pages-- 
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/pomodoro')
def pomodoro():
    return render_template('pomodoro.html')

@app.route('/planner')
def planner():
    return render_template('planner.html')

#--Run the app--
if_name_=='_main_':
	app.run(debug=True)
	