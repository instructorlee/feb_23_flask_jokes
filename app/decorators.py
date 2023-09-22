from flask import jsonify, request, session, redirect
from functools import wraps

from app.models.user import User

def login_required(function):
    @wraps(function)

    def wrap(*args, **kwargs): #  

        if 'user_id' in session:
            user = User.get_by_id(int(session['user_id']))

            if user:
                return function(user=user, *args, **kwargs)
        
        return redirect('/')

    return wrap 