from app import app
from app.controllers import jokes, home, users


if __name__=="__main__":
    app.run(debug=True)