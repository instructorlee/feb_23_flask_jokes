from flask import render_template, request, redirect, flash
from app.models.joke import Joke

from app import app

@app.route('/')
def display_home():
    return render_template('home.html')