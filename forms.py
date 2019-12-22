# -*- coding: utf-8 -*-
import re

from flask_wtf import FlaskForm
from wtforms import (BooleanField, FileField, FloatField, HiddenField,
                     IntegerField, PasswordField, RadioField, SelectField,
                     SelectMultipleField, StringField, SubmitField,
                     TextAreaField, validators, widgets)
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


auth_type_choices = [('3', 'Team Leader'),
                     ('4', 'Subteam Leader'),
                     ('1', 'Member')]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SQLForm(FlaskForm):
    query = TextAreaField('SQL to be run', validators=[DataRequired()])
    submit = SubmitField('Run query')


class EditEventForm(FlaskForm):
    name = StringField("Event Name")
    url = StringField("Url")
    location = StringField("Location")
    city = StringField("City")
    image = StringField("Image")
    date = DateField('Date', format='%Y-%m-%d')
    type_ = StringField("Type")
    description = StringField("Description")
    submit_event = SubmitField("Update Event")

class AddEventForm(FlaskForm):
    name = StringField("Event Name")
    ticket_url = StringField("Url")
    location = StringField("Location")
    city = StringField("City")
    image = StringField("Image")
    date = DateField('Date', format='%Y-%m-%d')
    e_type = StringField("Type")
    description = StringField("Description")
    add_event = SubmitField("Add Event")


class UploadCVForm(FlaskForm):
    cv = FileField('CV File')


class UploadImageForm(FlaskForm):
    image = FileField('Image File')
