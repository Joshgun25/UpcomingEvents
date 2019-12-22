import math
import os
import time
from datetime import datetime

import psycopg2 as db
from flask import (Blueprint, Flask, abort, flash, redirect, render_template,
				   request, send_from_directory, session, url_for)
from werkzeug.utils import secure_filename

import requests
from forms import (EditEventForm, AddEventForm)

organizer = Blueprint(name='organizer', import_name=__name__)


@organizer.route("/myevents/")
@organizer.route("/myevents")
def myevents_page():
	if (session.get('auth_type') == 'organizer'):
		result = requests.get("https://ituse19-uep.herokuapp.com/api/org_events/{}".format(session.get('organizer_id')))

		return render_template('organizer_myevents_page.html', myevents = result.json())
	else:
		return redirect(url_for('home.home_page'))


@organizer.route("/organizer/event/edit/<id>", methods=['GET', 'POST'])
def organizer_edit_event_page(id):
	
	if(session.get('auth_type') == 'organizer'):

		r = requests.get("https://ituse19-uep.herokuapp.com/api/event_detail/{}".format(id))
		event_data = r.json()
		
		form = EditEventForm()
		if (request.method == 'POST' and form.submit_event.data or form.validate()):
			name = form.name.data.encode('utf-8')
			date = form.date.data
			description = form.description.data.encode('utf-8')
			url = form.url.data.encode('utf-8')
			image = form.image.data
			location = form.location.data.encode('utf-8')
			city = form.city.data.encode('utf-8')
			type_ = form.type_.data.encode('utf-8')

			URL = "https://ituse19-uep.herokuapp.com/api/event_update"
			PARAMS = {'old_event_id': id, 'name': name, 'date': date, 'description': description, 'ticket_url':url, 'image': image, 'location': location, 'city': city, 'e_type': type_, 'org_id': session.get('organizer_id')}
			r = requests.post(url=URL,params = PARAMS)
			result = r.json()
			if result['result'] == 1:
				print(result['message'])

			return redirect(url_for('organizer.organizer_edit_event_page', id=id))
		else:
			if(session.get('auth_type') != 'organizer'):
				flash('No organizer privileges...', 'danger')
				return redirect(url_for('home.home_page'))

			r2 = requests.get("https://ituse19-uep.herokuapp.com/api/event_detail/{}".format(id))
			event_data2 = r2.json()[0]
			form.name.data = event_data2['name']
			form.date.data = event_data2['date']
			form.description.data = event_data2['description']
			form.url.data = event_data2['url']
			form.image.data = event_data2['image']
			form.location.data = event_data2['location']
			form.city.data = event_data2['city']
			form.type_.data = event_data2['type']

			return render_template('organizer_edit_event_page.html', form=form, result=event_data2)
		return render_template('organizer_edit_event_page.html', form=form, result=event_data[0])
	
	else:
		flash('No organizer privileges...', 'danger')
		return redirect(url_for('home.home_page'))

@organizer.route("/admin/add/team", methods=['GET', 'POST'])
def organizer_add_event_page():
	if(session.get('auth_type') != 'organizer'):
		flash('No organizer privileges...', 'danger')
		return redirect(url_for('home.home_page'))
	else:
		form = AddEventForm()
		if (request.method == 'POST' and form.add_event.data or form.validate()):
			name = form.name.data
			ticket_url = form.ticket_url.data
			location = form.location.data
			city = form.city.data
			image = form.image.data
			date = form.date.data
			e_type = form.e_type.data
			description = form.description.data
			

			URL = "https://ituse19-uep.herokuapp.com/api/add_new_event/{}".format(session.get('organizer_id'))
			PARAMS = {'name': name, 'date': date, 'description': description, 'ticket_url':ticket_url, 'image': image, 'location': location, 'city': city, 'type': e_type}
			r = requests.post(url=URL,params = PARAMS)
			data = r.json()
			print(data)

			return redirect(url_for('organizer.organizer_add_event_page'))
		return render_template('organizer_add_event_page.html',form=form)