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

class OrganizerProfile(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    org_id = IntegerField("ID")
    address = StringField("Adddress")

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField("Name")
    email = StringField('Email')
    address = StringField('Address')
    submit_reg = SubmitField('Signup')

