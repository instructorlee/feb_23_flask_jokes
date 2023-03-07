from flask import render_template, request, redirect, flash
from app.models.joke import Joke

from app import app

@app.route('/')
def display_home():
    return render_template('home.html')

@app.route('/joke/add')
def get_add_joke_form():
    return render_template('add.html')

@app.route('/joke/<int:id>')
def get_by_id(id):
    return render_template('view.html', joke=Joke.get_by_id(id))

@app.route('/joke/add', methods=['POST'])
def add_joke():
    Joke.create({
        'text': request.form['joke'], 
        'punchline': request.form['punchline'],
        })
    flash('Your Joke has been added.')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    t = Joke.get_all()
    return render_template('dashboard.html', rows=Joke.get_all())

@app.route('/joke/<int:id>')
def get_joke(id):
    return render_template('view.html', joke=Joke.get_by_id(id))

@app.route('/joke/update/<int:id>')
def get_update_joke_form(id):
    return render_template('update.html', joke=Joke.get_by_id(id))

@app.route('/joke/update', methods=['POST'])
def update_joke():
    Joke.update({
        'id': int(request.form['id']), 
        'text': request.form['joke'], 
        'punchline': request.form['punchline']
        })
        
    flash('Your Joke has been updated.')
    return redirect('/dashboard')

@app.route('/joke/delete/<int:id>')
def delete_joke(id):
    Joke.delete(id)
    flash('Your Joke has been deleted.')
    return redirect('/dashboard')

@app.errorhandler(404)
def handle_404(e):
    return "You're lost, get a map!"