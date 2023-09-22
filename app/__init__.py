from flask import Flask


UPLOAD_FOLDER = '/Users/leeloftiss/Desktop/cd/class_files/feb_23_flask_jokes/app/uploads'


app = Flask(__name__)

app.secret_key = 'abc123!%&'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER