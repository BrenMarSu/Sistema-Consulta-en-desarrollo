from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/imagen')
def imagen():
    return render_template('imagen.html')

@app.route('/templates/images/logo_tecnm-removebg-preview.png')
def get_logo():
    return app.send_templates_file('images/logo_tecnm-removebg-preview.png')
