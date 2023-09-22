import os
from flask import render_template, request, redirect, flash, session, url_for, send_from_directory
from app.models.joke import Joke
from app.models.punchline import Punchline
from app.models.user import User
from app.decorators import login_required
from werkzeug.utils import secure_filename

from app import app

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

@app.route('/joke/add')
@login_required
def get_add_joke_form(user):
    
    return render_template('add.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/joke/add', methods=['POST'])
@login_required
def add_joke(user):

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect('/dashboard')

    Joke.create({
        'user_id': session['user_id'],
        'text': request.form['text'], 
        'punchline': request.form['punchline'],
        })
    flash('Your Joke has been added.')
    return redirect('/dashboard')

@app.route('/uploads')
def download_file():
    return send_from_directory(app.config["UPLOAD_FOLDER"], '81L0HoszayL._AC_SL1500_.jpg')

@app.route('/dashboard')
@login_required
def dashboard(user):
    
    return render_template('dashboard.html', rows=Joke.get_all(session['user_id']))

@app.route('/joke/<int:id>')
@login_required
def get_joke(id, *args, **kwargs):

    return render_template('view.html', joke=Joke.get_with_likes(id))

@app.route('/joke/like/<int:joke_id>')
def like_joke(joke_id):
    Joke.like(joke_id, session['user_id'])
    return redirect(f'/dashboard')

@app.route('/joke/unlike/<int:joke_id>')
def unlike_joke(joke_id):
    Joke.unlike(joke_id, session['user_id'])
    return redirect(f'/dashboard')

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