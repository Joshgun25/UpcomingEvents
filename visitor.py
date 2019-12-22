# -*- coding: utf-8 -*-
import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

from forms import *
from queries import select
import requests

visitor = Blueprint(name='visitor', import_name=__name__,
                    template_folder='templates')

# TODO:: IMPLEMENT SMALL LOGO OF EACH ROUTE'S ELEMENTS

@visitor.route("/contact")
@visitor.route("/contact/")
def visitor_contact_page():
    return render_template('contact_page.html')


@visitor.route("/eventinfo/<event_id>")
def visitor_eventinfo_page(event_id):
    result = requests.get("https://ituse19-uep.herokuapp.com/api/event_detail/{}".format(event_id))


    return render_template('eventinfo_page.html', result=result.json())