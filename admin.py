# -*- coding: utf-8 -*-
import math
import os
import time
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

import requests

admin = Blueprint(name='admin', import_name=__name__)


@admin.route("/admin/")
@admin.route("/admin")
def admin_page():
	if (session.get('member_id') == 'admin'):
		return render_template('admin_page.html')
	else:
		return redirect(url_for('home.home_page'))


@admin.route("/admin/organizers", methods=['GET', 'POST'])
def admin_organizers_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		result = requests.get("https://ituse19-uep.herokuapp.com/api/admin/all_organizers/")
		return render_template('admin_organizers_page.html', organizers=result.json())




@admin.route("/admin/review/events", methods=['GET'])
def admin_review_events_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		result = requests.get("https://ituse19-uep.herokuapp.com/api/admin/event_review")
		return render_template('admin_review_events_page.html', result=result.json())


@admin.route("/admin/reject/event/<id>", methods=['GET','DELETE'])
def admin_reject_event(id):
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		requests.delete("https://ituse19-uep.herokuapp.com/api/admin/event_reject/{}".format(id))
		return redirect(url_for('admin.admin_review_events_page'))

@admin.route("/admin/approve/event/<id>", methods=['GET','POST'])
def admin_approve_event(id):
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		requests.post("https://ituse19-uep.herokuapp.com/api/admin/new_event_approve/{}".format(id))
		return redirect(url_for('admin.admin_review_events_page'))




@admin.route("/admin/review/organizers", methods=['GET', 'POST'])
@admin.route("/admin/review/organizers/", methods=['GET', 'POST'])
def admin_review_organizers_page():
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		result = requests.get("https://ituse19-uep.herokuapp.com/api/admin/organizer_review")
		return render_template('admin_review_organizers_page.html', result=result.json())


@admin.route("/admin/reject/organizer/<id>", methods=['GET','DELETE'])
def admin_reject_organizer(id):
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		requests.delete("https://ituse19-uep.herokuapp.com/api/admin/organizer_reject/{}".format(id))
		return redirect(url_for('admin.admin_review_organizers_page'))

@admin.route("/admin/approve/organizer/<id>", methods=['GET', 'POST'])
def admin_approve_organizer(id):
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		requests.post("https://ituse19-uep.herokuapp.com/api/admin/organizer_approve/{}".format(id))
		return redirect(url_for('admin.admin_review_organizers_page'))

