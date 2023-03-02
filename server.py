from flask import Flask, render_template, request, redirect, flash

from models.joke import Joke

app = Flask(__name__)
app.secret_key = 'abc123!%&'


@app.route('/')
def display_home():
    return render_template('home.html', joke = Joke.get_by_id(1))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', rows=Joke.get_all())

@app.route('/joke/view/<int:id>')
def view_joke(id):
    return render_template('view.html', joke=Joke.get_by_id(id))

@app.route('/joke/add') # default == GET
def get_add_joke_form():
    return render_template('add.html')

@app.route('/joke/add', methods=['POST'])
def add_joke():
    Joke.create(request.form['text'], request.form['punchline'])
    flash('Your Joke has been added.')
    return redirect('/dashboard')

@app.route('/joke/delete/<int:id>') # default == GET
def delete_joke(id):
    Joke.delete(id)
    return redirect('/dashboard')

@app.errorhandler(404)
def handle_404(e):
    return "You're lost, get a map!"

if __name__=="__main__":
    app.run(debug=True)