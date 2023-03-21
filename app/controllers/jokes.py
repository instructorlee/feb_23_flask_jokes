from flask import render_template, request, redirect, flash, session
from app.models.joke import Joke
from app.models.punchline import Punchline
from app.models.user import User

from app import app

@app.route('/joke/add')
def get_add_joke_form():

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('add.html')

@app.route('/joke/add', methods=['POST'])
def add_joke():

    if 'user_id' not in session:
        return redirect('/')
    
    Joke.create({
        'user_id': session['user_id'],
        'text': request.form['text'], 
        'punchline': request.form['punchline'],
        })
    flash('Your Joke has been added.')
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session: # session['user_id']
        flash('Please log in.')
        return redirect('/')
    
    return render_template('dashboard.html', rows=Joke.get_all())

@app.route('/joke/<int:id>')
def get_joke(id):

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('view.html', joke=Joke.get_by_id(id))

@app.route('/joke/update/<int:id>')
def get_update_joke_form(id):

    if 'user_id' not in session:
        return redirect('/')
    
    joke = Joke.get_by_id(id)

    if not joke or joke.user_id != session['user_id']:
        return redirect('/')
    
    return render_template('update.html', joke=joke)

@app.route('/joke/update/', methods=['POST'])
def update_joke():

    if 'user_id' not in session:
        return redirect('/')
    
    joke = Joke.get_by_id(id)

    if not joke or joke.user_id != session['user_id']:
        return redirect('/')
    
    Joke.update({ 
        'id': request.form['id'], 
        'text': request.form['text'], 
        'punchline': request.form['punchline']
        })
        
    flash('Your Joke has been updated.')
    return redirect('/dashboard')

@app.route('/joke/delete/<int:id>')
def delete_joke(id):

    if 'user_id' not in session:
        return redirect('/')
    
    Joke.delete(id)
    flash('Your Joke has been deleted.')
    return redirect('/dashboard')

@app.route('/joke/my-jokes')
def my_jokes():

    if 'user_id' not in session:
        return redirect('/')
    
    return render_template('my_jokes.html', user=User.get_by_id(session['user_id']))

@app.route('/joke/add-punchline', methods=['POST'])
def add_punchline():

    if 'user_id' not in session:
        return redirect('/')
    
    Punchline.create({
        'text': request.form['text'], 
        'joke_id': request.form['joke_id'],
        })
    flash('Your punchline has been added.')
    return redirect(f"/joke/update/{request.form['joke_id']}") # /joke/update/<id of the joke>

@app.route('/joke/remove-punchline/<int:id>')
def delete_punchline(id):

    if 'user_id' not in session:
        return redirect('/')
    
    punchline = Punchline.get_by_id(id)

    if punchline:
        Punchline.delete(id)
        flash('Your punchline has been deleted.')
        return redirect(f"/joke/update/{punchline.joke_id}")

    return redirect('/dashboard')

@app.errorhandler(404)
def handle_404(e):
    return "You're lost, get a map!"