
from app import app
from app.model import Vocabulary
from app.model import QuizParameters
from ._utils import resolve_icon
from ._utils import kana_reference_tables
from ._utils import BATON
from flask import redirect
from flask import render_template
from flask import request
from app.forms import QuizSetupForm1
from app.forms import QuizSetupForm2a
from app.forms import QuizSetupForm2b
from app.forms import QuizSetupForm3
from app.forms import QuizSetupForm4
from app.forms import QuizSetupForm5
from app.forms import QuizSetupForm6


@app.route('/')
@app.route('/index')
@app.route('/vocab')
def index():
    return render_template('vocabulary.html',
                           words=Vocabulary(),
                           title='Vocabulary',
                           emoji=resolve_icon('backpack'))


@app.route('/kana')
def kana():
    return render_template('kana.html', reftabs=kana_reference_tables(), title='Kana', emoji=resolve_icon('brilliance'))


@app.route('/quiz_setup', methods=['GET', 'POST'])
def quiz_setup():
    form = QuizSetupForm1()
    if form.validate_on_submit():
        params = QuizParameters()
        params.table = form.table.data
        BATON.object = params
        return redirect('/quiz_setup2')
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup2', methods=['GET', 'POST'])
def quiz_setup2():
    params = BATON.object
    form = QuizSetupForm2a() if params.table == 'Vocabulary' else QuizSetupForm2b()
    if form.validate_on_submit():
        params.type_of_quiz = form.quiz_type.data
        BATON.object = params
        return redirect('/quiz_setup3')
    BATON.object = params
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup3', methods=['GET', 'POST'])
def quiz_setup3():
    params = BATON.object
    form = QuizSetupForm3()
    if form.validate_on_submit():
        params.number_of_items = int(form.number_of_items.data)
        BATON.object = params
        return redirect('/quiz_setup4')
    BATON.object = params
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup4', methods=['GET', 'POST'])
def quiz_setup4():
    params = BATON.object
    form = QuizSetupForm4()
    if form.is_submitted():  # form.validate_on_submit() doesn't come back True when the submit button is clicked
        params.prompt_type = form.prompt_type.data
        BATON.object = params
        return redirect('/quiz_setup5')
    choices = ['English', 'Kana', 'Kanji'] if params.table == 'Vocabulary' else ['Romaji', 'Hiragana', 'Katakana']
    form.prompt_type.choices = choices
    BATON.object = params
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup5', methods=['GET', 'POST'])
def quiz_setup5():
    params = BATON.object
    form = QuizSetupForm5()
    if form.is_submitted():  # form.validate_on_submit() doesn't come back True when the submit button is clicked
        params.choice_type = form.choice_type.data
        BATON.object = params
        return redirect('/quiz_setup6')

    # Create the list of possible choice types
    # The user should be presented with the set of "word" forms *except* the "word" form chosen for quiz item prompts
    choices = ['English', 'Kana', 'Kanji'] if params.table == 'Vocabulary' else ['Romaji', 'Hiragana', 'Katakana']
    form.choice_type.choices = [c for c in choices if c != params.prompt_type]

    BATON.object = params
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup6', methods=['GET', 'POST'])
def quiz_setup6():
    params = BATON.object
    form = QuizSetupForm6(request.form)
    if request.method == 'POST':
        if form.cancel.data:
            BATON.drop()
            return redirect('/index')
        elif form.is_submitted():
            BATON.object = params
            return redirect('/multiple_choice_quiz')
    BATON.object = params
    return render_template('quiz_start.html', form=form, quiz_params=params,
                           title='Quiz Setup', emoji=resolve_icon('question'))