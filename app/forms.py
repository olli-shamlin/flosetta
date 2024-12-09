
from flask_wtf import FlaskForm
from wtforms import SubmitField
# TODO OBSOLETE from wtforms import RadioField
from wtforms import StringField
from wtforms.widgets import HiddenInput


# TODO OBSOLETE class QuizSetupForm1(FlaskForm):
# TODO OBSOLETE     """Choose type of table"""
# TODO OBSOLETE     # TODO populate choices list using TableOption
# TODO OBSOLETE     table = RadioField('What do you want to be quizzed on?', choices=['Vocabulary', 'Syllabary'])
# TODO OBSOLETE     submit = SubmitField('Continue')
# TODO OBSOLETE
# TODO OBSOLETE
# TODO OBSOLETE class QuizSetupForm2a(FlaskForm):
# TODO OBSOLETE     """Choose type of quiz for Vocabulary"""
# TODO OBSOLETE     # TODO populate choices list using QuizTypeOption
# TODO OBSOLETE     quiz_type = RadioField('What kind of quiz do you want?', choices=['Multiple Choice', 'Match'])
# TODO OBSOLETE     submit = SubmitField('Continue')
# TODO OBSOLETE
# TODO OBSOLETE
# TODO OBSOLETE class QuizSetupForm2b(FlaskForm):
# TODO OBSOLETE     """Choose type of quiz for Kana"""
# TODO OBSOLETE     # TODO populate choices list using QuizTypeOption
# TODO OBSOLETE     quiz_type = RadioField('What kind of quiz do you want?', choices=['Multiple Choice', 'Match', 'Jigsaw', 'Memory'])
# TODO OBSOLETE     submit = SubmitField('Continue')
# TODO OBSOLETE
# TODO OBSOLETE
# TODO OBSOLETE class QuizSetupForm3(FlaskForm):
# TODO OBSOLETE     """Choose number of items to include in quiz"""
# TODO OBSOLETE     # TODO populate choices list using SizeOption
# TODO OBSOLETE     number_of_items = RadioField('How many items do you want in the quiz?', choices=[5, 10, 15, 20])
# TODO OBSOLETE     submit = SubmitField('Continue')
# TODO OBSOLETE
# TODO OBSOLETE
# TODO OBSOLETE class QuizSetupForm4(FlaskForm):
# TODO OBSOLETE     """Choose word form for PROMPT; this form's prompt_type choices are set by the calling view"""
# TODO OBSOLETE     prompt_type = RadioField('What word form do you want to be prompted with?', choices=['PLACEHOLDER'])
# TODO OBSOLETE     submit = SubmitField('Continue')
# TODO OBSOLETE
# TODO OBSOLETE
# TODO OBSOLETE class QuizSetupForm5(FlaskForm):
# TODO OBSOLETE     """Choose word form for CHOICES; this form's choice_types choices are set bye the calling view"""
# TODO OBSOLETE     choice_type = RadioField('What word form do you want to for choices?', choices=['PLACEHOLDER'])
# TODO OBSOLETE     submit = SubmitField('Continue')
# TODO OBSOLETE
# TODO OBSOLETE
# TODO OBSOLETE class QuizSetupForm6(FlaskForm):
# TODO OBSOLETE     """This form is used in conjunction with the quiz setup summary page."""
# TODO OBSOLETE     cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})
# TODO OBSOLETE     submit = SubmitField('Start')
# TODO OBSOLETE
# TODO OBSOLETE
class QuizSetupForm(FlaskForm):
    transport = StringField(id='transport', default='PLACEHOLDER', widget=HiddenInput())
    submit = SubmitField('Start')


class QuizForm(FlaskForm):
    transport = StringField(id='transport', default='PLACEHOLDER', widget=HiddenInput())
    submit = SubmitField('DONE')
# TODO OBSOLETE
# TODO OBSOLETE class MultipleChoiceQuizForm(FlaskForm):
# TODO OBSOLETE     responses = StringField(id='hidden-response-field', default='PLACEHOLDER', widget=HiddenInput())
# TODO OBSOLETE     submit = SubmitField('DONE')
