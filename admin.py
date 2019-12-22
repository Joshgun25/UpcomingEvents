# -*- coding: utf-8 -*-
import math
import os
import time
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename


from member_profile import Member
from queries import run, select, update
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


@admin.route("/admin/edit/event/<id>", methods=['GET', 'POST'])
def admin_edit_event_page(id):
	event_data = requests.get("https://ituse19-uep.herokuapp.com/api/event_detail/{}".format(id))


	form = EditCompetitionForm()
	imageForm = UploadImageForm()
	imageFolderPath = os.path.join(os.getcwd(), 'static/images/competitions')

	if (request.method == 'POST' and form.submit_competition.data or form.validate()):
		print("Not")
		name = form.name.data.encode('utf-8')
		date = form.date.data
		country = form.country.data.encode('utf-8')
		description = form.description.data.encode('utf-8')
		reward = form.reward.data.encode('utf-8')
		image = imageForm.image.data
		if(image and '.jpg' in image.filename or '.jpeg' in image.filename):
			current_date = time.gmtime()
			filename = secure_filename(
				"{}_{}.jpg".format(id, current_date[0:6]))
			filePath = os.path.join(imageFolderPath, filename)
			images = os.listdir(imageFolderPath)
			digits = int(math.log(int(id), 10))+1
			for im in images:
				if(im[digits] == '_' and im[0:digits] == str(id)):
					os.remove(os.path.join(imageFolderPath, im))
			image.save(filePath)
		elif(image):
			flash('Please upload a file in JPG format', "danger")
		print("Before update: ", date)
		update("competition", "name='{}', date=DATE('{}'), country='{}', description='{}', reward='{}'".format(
			name, date, country, description, reward), "id={}".format(id))
		return redirect(url_for('admin.admin_edit_event_page', id=id))
	else:
		if(session.get('member_id') != 'admin'):
			flash('No admin privileges...', 'danger')
			return redirect(url_for('home.home_page'))

		for event in event_data:
			if(event['id'] == id):
				result = event

		img_name = None
		for img in os.listdir(imageFolderPath):
			if(id in img[0:len(id)] and (img[len(id)] == '_' or img[len(id)] == '.')):
				img_name = img
		form.description.data = result['description']
		return render_template('admin_edit_event_page.html', form=form, result=result, imgName=img_name, uploadImg=imageForm)
	return render_template('admin_edit_event_page.html', form=form, result=result, imgName=img_name, uploadImg=imageForm)






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
		return render_template('admin_review_events_page.html')


@admin.route("/admin/approve/event/<id>", methods=['GET','POST'])
def admin_approve_event(id):
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		requests.post("https://ituse19-uep.herokuapp.com/api/admin/new_event_approve/{}".format(id))
		return render_template('admin_review_events_page.html')



@admin.route("/admin/review/organizers", methods=['GET', 'POST'])
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
		return render_template('admin_review_organizers_page.html')


@admin.route("/admin/approve/organizer/<id>", methods=['GET', 'POST'])
def admin_approve_organizer(id):
	if not session.get('logged_in'):
		return redirect(url_for('home.home_page'))
	else:
		requests.post("https://ituse19-uep.herokuapp.com/api/admin/organizer_approve/{}".format(id))
		return render_template('admin_review_organizers_page.html')


