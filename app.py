#Libreria para usar Flask y sesion
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
#Libreria para la autenticación de clave de acceso
from flask_httpauth import HTTPBasicAuth#, HTTPTokenAuth
#Libreria para el cierre de sesion despues de determinado tiempo
from flask_session import Session
from datetime import timedelta
#Libreria para la conexión con la base de datos
import psycopg2


app = Flask(__name__, template_folder='templates')

#autenticación
auth = HTTPBasicAuth()
#auth = HTTPTokenAuth(scheme='Bearer')

# Configurar la sesión con el módulo flask_session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)
Session(app)

# Conexión a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="SIE",
    user="postgres",
    password="Br3nd4"
)

@auth.verify_password
def verify_password(username, password):
    # Aquí deberás verificar el usuario y la contraseña
    if username == 'SuperUsuario' and password == 'ARGMEC':
        return "Acesso concedido"
        
    return False

@app.route('/', methods=['GET', 'POST'])
@auth.login_required
def index():
    # Si la solicitud es POST, significa que se hizo clic en el botón "Cerrar sesión"
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('login'))
    # Si la sesión está activa, renderiza la página protegida
    if 'username' in session:
        return render_template('protected.html') 
    # Si la sesión no está activa, redirige al inicio de sesión
    return redirect(url_for('login'))

    #return "¡Acceso concedido!"

# Ruta de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si la solicitud es POST, significa que se enviaron los datos del formulario de inicio de sesión
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Aquí va la lógica de verificación de usuario y contraseña
        if username == 'SuperUsuario' and password == 'ARGMEC': # Reemplaza esto por tu lógica de verificación de usuario y contraseña
            session['username'] = username
            session.permanent = True
            app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
            return redirect(url_for('index'))
    # Si la sesión está activa, redirige a la página protegida
    if 'username' in session:
        return render_template('protected.html') 
    # Si la sesión no está activa, renderiza la página de inicio de sesión
    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Ruta para obtener los alumnos que estan vigentes
@app.route('/alumnos/<sta>', methods=['GET'])
@auth.login_required
def obtener_alumnos(sta):

    cursor = conn.cursor()
    cursor.execute(
        "SELECT numcon, apepat, apemat, nom, sta  FROM alumnos WHERE sta=1",
        (sta,)
    )
    alumnos = cursor.fetchall()
    cursor.close()
    return jsonify(alumnos)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
