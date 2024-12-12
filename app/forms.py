
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import StringField
from wtforms.widgets import HiddenInput


class QuizSetupForm(FlaskForm):
    transport = StringField(id='transport', default='PLACEHOLDER', widget=HiddenInput())
    submit = SubmitField('Start')


class QuizForm(FlaskForm):
    transport = StringField(id='transport', default='PLACEHOLDER', widget=HiddenInput())
    submit = SubmitField(id='submit-btn', label='Done')
