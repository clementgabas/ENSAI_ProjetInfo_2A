from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')


def home():
    return render_template('Page/home.html')

@app.route('/friends')
def friends():
    return render_template('Page/friends.html')

if __name__ == '__main__' :
    app.run(debug=True, port=666)
