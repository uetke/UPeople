from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email


class NewCourseForm(FlaskForm):
    name = StringField('Course Name')
    start_date = DateField('Start Date')
    end_date = DateField('End Date')


class NewContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name')
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Send')