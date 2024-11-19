
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms import RadioField
from wtforms import StringField
from wtforms.widgets import HiddenInput


class QuizSetupForm1(FlaskForm):
    """Choose type of table"""
    # TODO populate choices list using TableOption
    table = RadioField('What do you want to be quizzed on?', choices=['Vocabulary', 'Syllabary'])
    submit = SubmitField('Continue')


class QuizSetupForm2a(FlaskForm):
    """Choose type of quiz for Vocabulary"""
    # TODO populate choices list using QuizTypeOption
    quiz_type = RadioField('What kind of quiz do you want?', choices=['Multiple Choice', 'Match'])
    submit = SubmitField('Continue')


class QuizSetupForm2b(FlaskForm):
    """Choose type of quiz for Kana"""
    # TODO populate choices list using QuizTypeOption
    quiz_type = RadioField('What kind of quiz do you want?', choices=['Multiple Choice', 'Match', 'Jigsaw', 'Memory'])
    submit = SubmitField('Continue')


class QuizSetupForm3(FlaskForm):
    """Choose number of items to include in quiz"""
    # TODO populate choices list using SizeOption
    number_of_items = RadioField('How many items do you want in the quiz?', choices=[5, 10, 15, 20])
    submit = SubmitField('Continue')


class QuizSetupForm4(FlaskForm):
    """Choose word form for PROMPT; this form's prompt_type choices are set by the calling view"""
    prompt_type = RadioField('What word form do you want to be prompted with?', choices=['PLACEHOLDER'])
    submit = SubmitField('Continue')


class QuizSetupForm5(FlaskForm):
    """Choose word form for CHOICES; this form's choice_types choices are set bye the calling view"""
    choice_type = RadioField('What word form do you want to for choices?', choices=['PLACEHOLDER'])
    submit = SubmitField('Continue')


class QuizSetupForm6(FlaskForm):
    """This form is used in conjunction with the quiz setup summary page."""
    cancel = SubmitField('Cancel', render_kw={'formnovalidate': True})
    submit = SubmitField('Start')


class MultipleChoiceQuizForm(FlaskForm):
    responses = StringField(id='hidden-response-field', default='initial string field value', widget=HiddenInput())
    submit = SubmitField('DONE')
