import os

import psycopg2 as db
import psycopg2.extensions
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, send_from_directory, session, url_for)

from admin import admin
from organizer import organizer
from dbinit import initialize
from home import home
from login import login
from sign_up import sign_up
from visitor import visitor
from panel import panel

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

RELEASE = True

if(not RELEASE):
    os.environ['DATABASE_URL'] = "postgres://postgres:docker@localhost:5432/postgres"
    initialize(os.environ.get('DATABASE_URL'))

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW'

app.register_blueprint(home)
app.register_blueprint(organizer)
app.register_blueprint(login)
app.register_blueprint(admin)
app.register_blueprint(visitor)
app.register_blueprint(panel)
app.register_blueprint(sign_up)

@app.errorhandler(404)
def not_found(e):
    return render_template("error_404.html")

if __name__ == "__main__":
    if(not RELEASE):
        app.run(debug=True)
    else:
        app.run()
