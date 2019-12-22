# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import select
import requests
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

home = Blueprint(name='home', import_name=__name__,
                    template_folder='templates')

# TODO:: IMPLEMENT SMALL LOGO OF EACH ROUTE'S ELEMENTS


@home.route("/", methods=['GET'])
def home_page():
    event_data = requests.get("https://ituse19-uep.herokuapp.com/api/events/1000")
    return render_template("home_page.html", events=event_data.json())