from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if password != password2:
            message = 'Contraseñas no coinciden'
            print(message)
            return render_template('register.html')



    return render_template('register.html')

@app.route('/recover')
def recover():
    return render_template('recover.html')