# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
from forms import SignupForm
import psycopg2 as db
from Crypto.Hash import SHA256
import os
import requests

sign_up = Blueprint(name='sign_up', import_name=__name__,
                  template_folder='templates')



@sign_up.route("/signup", methods=['GET', 'POST'])
def sign_up_page():
    if session.get('logged_in'):
        return redirect(url_for('home.home_page'))
    else:
        form = SignupForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            address = form.address.data
            name = form.name.data
        
            URL = "https://ituse19-uep.herokuapp.com/api/register_organizer"
            PARAMS = {'name': name, 'username': username, 'password': password, 'mail': email, 'address': address}
            r = requests.post(url=URL,params = PARAMS)
            return redirect(url_for('home.home_page'))
        return render_template('signup_page.html', form=form)

    