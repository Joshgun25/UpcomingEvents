# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for, flash, request, session, abort, Blueprint
from forms import LoginForm
import psycopg2 as db
from Crypto.Hash import SHA256
import os
import requests

login = Blueprint(name='login', import_name=__name__,
                  template_folder='templates')


@login.route("/login", methods=['GET', 'POST'])
def login_page():
    if session.get('logged_in'):
        return redirect(url_for('home.home_page'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            organizerLoginSuccess = checkOrganizerLogin(username, password)
            if(not organizerLoginSuccess):
                adminLogin = checkAdminLogin(username, password)
            if(organizerLoginSuccess or adminLogin):
                return redirect(url_for('home.home_page'))
        return render_template('login_page.html', form=form)

@login.route("/logout")
def logout_page():
    if 'logged_in' in session:
        try:
            session.pop('username', None)
            session['organizer_id'] = 0
            session.pop('logged_in', None)
            session.pop('member', None)
            session['auth_type'] = None
            flash('You have been successfully logged out.', 'success')

        except:
            flash('Logging out is not completed.')
    return redirect(url_for('home.home_page'))


def checkOrganizerLogin(username, password):
    success = False
    URL = "https://ituse19-uep.herokuapp.com/api/organizer_login_verif"
    PARAMS = {'username': username, 'password': password}
    response = requests.get(url = URL, params = PARAMS)

    if(response.json()['result'] == 1):
        flash('You have been logged in!', 'success')
        session['logged_in'] = True
        session['organizer_id'] = response.json()['org_id']
        session['auth_type'] = 'organizer'
        success = True
        return redirect(url_for('home.home_page'))
    return success


def checkAdminLogin(username, password):
    success = False
    URL = "https://ituse19-uep.herokuapp.com/api/admin/login_verif"
    PARAMS = {'username': username, 'password': password}
    response = requests.get(url = URL, params = PARAMS)

    if(response.json()['result'] == 1):
        flash('You have been logged in!', 'success')
        session['logged_in'] = True
        session['auth_type'] = 'admin'
        success = True
        return redirect(url_for('home.home_page'))
    return success
