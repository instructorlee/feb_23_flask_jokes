from flask import render_template, request, redirect, flash, session
from app.models.user import User
from flask_bcrypt import Bcrypt 
from app import app

from app.config.mysqlconnection import connectToMySQL 
      
bcrypt = Bcrypt(app)

@app.route('/user/register', methods=['POST'])
def register():

    if User.validate_registration(request.form):

        User.create({
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email_address': request.form['email_address'],
            'password': bcrypt.generate_password_hash(request.form['password'])
            })
        flash('Thank you for registering')
    
    return redirect('/')

@app.route('/user/login', methods=['POST'])
def login():
    """
        validate 
            validate form in model

        Get user by email
            - Does it exist?
        validation
    """
    user = User.get_by_email(request.form['email_address'])

    if user == None or bcrypt.check_password_hash(user.password, request.form['password']) == False:
        flash("Invalid Credentials")
        return redirect('/')

    session['user_id'] = user.id
    flash("Welcome Back!")
    return redirect('/dashboard')

@app.route('/user/logout')
def logout():
    flash('Thank you for visiting today!')
    session.clear()
    return redirect('/')
