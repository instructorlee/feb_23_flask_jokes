import re
from flask import flash
from app.config.mysqlconnection import connectToMySQL   

from app.models.joke import Joke

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') # name@domain.com

class User:

    dB = 'z_jokes'

    def __init__(self, data):
        
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']

        self.jokes = []

    @classmethod
    def get_by_id(cls, id):
        
        query = """
            SELECT 
                * 
            FROM 
                users
                LEFT JOIN jokes ON jokes.user_id = users.id

            WHERE 
                users.id=%(id)s
                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, { 'id': id })

        if results:
            user = cls(results[0])
            
            for result in results:
                user.jokes.append(Joke({
                    'id': result['jokes.id'],
                    'user_id': result['user_id'],
                    'text': result['text'],
                    'date_added': result['date_added']
                }))

            return user

        return None
    
    @classmethod
    def get_by_email(cls, email_address):
        
        query = """
            SELECT 
                * 
            FROM 
                users

            WHERE 
                email_address=%(email_address)s
                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, { 'email_address': email_address })
        
        if not results:
            return None
        
        return cls(results[0])
        
        #return cls(results[0]) if results else None # double check that something was found

    @classmethod
    def get_all(cls):

        query = """
            SELECT 
                * 
            FROM 
             users;
        """

        results = connectToMySQL(cls.dB).query_db(query)

        """
        rows = []

        for result in results:
            rows.append(cls(result))

        return rows
        """

        return [cls(result) for result in results] # List Comprehension
        
    @classmethod
    def create(cls, data):

        query = """
            INSERT INTO

                users
                
            (first_name, last_name, email_address, password)
            
            VALUES
            (%(first_name)s, %(last_name)s, %(email_address)s, %(password)s)
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, data)

    @classmethod
    def update(cls, data):

        query = """
            UPDATE

                users
                
            SET
                first_name=%(first_name)s,
                last_name=%(last_name)s,
                email_address=%(email_address)s
            
            WHERE
                id=%(id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, data)

    @classmethod
    def delete(cls, id):
        
        query = """
        DELETE FROM 
            users

        WHERE
            id=%(id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, { 'id': id })

    @staticmethod
    def validate_registration(registration_form):

        """
            email is valid format
            last first names > 3 letters
            password requriements
            confirmation password
            unique email address
        """
        
        is_valid = True

        if User.get_by_email(registration_form['email_address']):
            is_valid = False
            flash("Email address already used.", "registration")

        if not EMAIL_REGEX.match(registration_form['email_address']):
            flash("Invalid Email Address", "register")
            is_valid = False

        if len(registration_form['first_name']) < 3:
            is_valid = False
            flash("Your first name is too short.", "registration")

        if len(registration_form['last_name']) < 3:
            is_valid = False
            flash("Your last name is too short.", "registration")

        if len(registration_form['password']) < 8:
            flash("Password must be at least 8 characters", "registration")
            is_valid = False

        if registration_form['password'] != registration_form['confirm_password']:
            is_valid = False
            flash("Your passwords don't match.", "registration")

        return is_valid
