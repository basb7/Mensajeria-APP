from email import message
from flask import Flask, flash, render_template, request, session, url_for, redirect
from markupsafe import escape
from datetime import datetime

import controler

app = Flask(__name__)
app.secret_key = 'my_secret_key {}'.format(datetime.now)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard/<user>')
def dashboard(user):
    return render_template('dashboard.html', user=(user))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        print(user)
        password = request.form['password']
        print(password)

    # Se valida si el usuario existe o esta registrado, inicio de sesión
        is_user = controler.validate_user(user)
        print(is_user)
        if is_user:
            if is_user[0]['USER'] == user or is_user[0]['EMAIL'] == user and is_user[0]['PASSWORD'] == str(password):
                session['username'] = user
                print('Usuario logueado')
                return redirect(url_for('dashboard', user = is_user[0]['USER']))
            return redirect(url_for('login'))
        else:
            message = 'Usuario no existe, intentelo de nuevo'
            flash(message, 'danger')
            print('Usuario no existe')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        message = 'Sesión finalizada exitosamente!'
        flash(message, 'success')
    return redirect(url_for('login'))

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

    # Valida los campos del formulario que no esten vacios
        if not email or not name or not username or not password or not password2:
            message = 'Los campos no pueden estar vacios, intente de nuevo!'
            flash(message, 'danger')
            return render_template('register.html')

    # Consulta la base de datos en busca de usuario o correos registrados en la base de datos
        if controler.validate_user(email) == False or controler.validate_user(username) == False:
            message = 'El correo o usuario ya estan registrados en nuestra base, intenta iniciar sesíon!'
            flash(message, 'warning')
            return render_template('register.html')

    # Valida que los campo password sean iguales
        if password != password2:
            message = 'Contraseñas no coinciden'
            print(message)
            flash(message, 'danger')
            return render_template('register.html')

    # Registro de usuario en la base de datos
        if controler.add_user(email, name, username, password) == True:
            print('Registro exitoso')
            message = 'Registro exitoso, inicie sesión'
            flash(message, 'success')
            return render_template('login.html')
        else:
            message = 'Error al registrar usuario'
            flash(message, 'danger')       
            print('Error al registrar usuario')

    return render_template('register.html')

@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        username = request.form['username']

        #Validar que los campos no esten vacios
        if not username:
            message = 'Los campos no pueden estar vacios, intente nuevamente!'
            flash(message, 'danger')
            return render_template('recover.html')

        #Validar si el usuario existe y enviar correo de recuperacion
        if controler.validate_user(username) == False:
            message = 'El usuario no existe, intente registrarse o intentelo de nuevo!'
            flash(message, 'danger')
            return render_template('recover.html')
        
        is_user = controler.validate_user(username)
        email_user = is_user[0]['EMAIL']

        def encode_email(email_user):
            length = 0
            count = 0
            arroba = False
            encode_email = ''

            for i in email_user:
                if i == '@':
                    break
                length += 1

            size = (int(length) / 1.5)
            
            for letra in email_user:
                if letra == '@':
                    arroba = True
                
                if count > size and arroba == False:
                    letra = '*'
                    encode_email += letra

                count += 1
                encode_email += letra
            
            return encode_email
        
        message = 'Se ha enviado correo de recuperacion a la siguiente dirección {}'.format(encode_email(email_user))
        flash(message, 'success')
        return render_template('recover.html')

    return render_template('recover.html')

#Proteccion de rutas
""" @app.before_request
def load_user():
    if "username" not in session and (request.endpoint not in ['index', 'login', 'register', 'recover']):
        print('Debe iniciar sesion')
        return redirect(url_for('login')) """