from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('Pages/home.html')

@app.route('/friends')
def friends():

    return render_template('Pages/friends.html')

if __name__ == '__main__':
    app.run (debug=True, port = 999)