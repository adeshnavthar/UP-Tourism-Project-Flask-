from flask import Flask,render_template,request,redirect
app = Flask(__name__)
app.secret_key = "Adesh"

from urls import *
from flask_mail import Mail,Message


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'uptoursandtravels@gmail.com'
app.config['MAIL_PASSWORD'] = 'gwse kpjj qxjr gszb'

mail = Mail(app)

if __name__ == "__main__":
    app.run(debug = True)