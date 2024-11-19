
from . import app
from .forms import QuizSetupForm1
from .forms import QuizSetupForm2a
from .forms import QuizSetupForm2b
from .forms import QuizSetupForm3
from .forms import QuizSetupForm4
from .forms import QuizSetupForm5
from .forms import QuizSetupForm6
from .forms import MultipleChoiceQuizForm
from .model import Vocabulary
from .model import Parameters
from .model import TableOption
from .model import create_quiz
from ._utils import resolve_icon
from ._utils import kana_reference_tables
from ._utils import BATON
from flask import redirect
from flask import render_template
from flask import request


@app.route('/')
@app.route('/index')
@app.route('/vocab')
def index():
    vocabulary = Vocabulary()
    return render_template('vocabulary.html',
                           words=vocabulary,
                           title='Vocabulary',
                           emoji=resolve_icon('backpack'))


@app.route('/kana')
def kana():
    return render_template('kana.html', reftabs=kana_reference_tables(), title='Kana', emoji=resolve_icon('brilliance'))


@app.route('/quiz_setup', methods=['GET', 'POST'])
def quiz_setup():
    form = QuizSetupForm1()
    if form.validate_on_submit():
        # TODO OBSOLETE params = QuizParameters()
        params = Parameters()
        params.table = form.table.data
        BATON.object = params
        return redirect('/quiz_setup2')
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup2', methods=['GET', 'POST'])
def quiz_setup2():
    params = BATON.object
    form = QuizSetupForm2a() if params.table == TableOption.VOCABULARY else QuizSetupForm2b()
    if form.validate_on_submit():
        # TODO OBSOLETE params.type_of_quiz = form.quiz_type.data
        params.kind = form.quiz_type.data
        BATON.object = params
        return redirect('/quiz_setup3')
    BATON.object = params
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup3', methods=['GET', 'POST'])
def quiz_setup3():
    params = BATON.object
    form = QuizSetupForm3()
    if form.validate_on_submit():
        # TODO OBSOLETE params.number_of_items = int(form.number_of_items.data)
        params.size = form.number_of_items.data
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
    # TODO OBSOLETE choices = ['English', 'Kana', 'Kanji'] if params.table == 'Vocabulary' else ['Romaji', 'Hiragana', 'Katakana']
    form.prompt_type.choices = params.prompt_options
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
    # TODO OBSOLETE choices = ['English', 'Kana', 'Kanji'] if params.table == 'Vocabulary' else ['Romaji', 'Hiragana', 'Katakana']
    # TODO OBSOLETE form.choice_type.choices = [c for c in choices if c != params.prompt_type]
    form.choice_type.choices = params.choice_options
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


@app.route('/multiple_choice_quiz', methods=['GET', 'POST'])
def multiple_choice_quiz():
    form = MultipleChoiceQuizForm()
    if form.validate_on_submit():
        quiz = BATON.object
        quiz.add_results(str(form.responses.data).split('|'))
        BATON.object = quiz
        return redirect('/quiz_results')
    params = BATON.object
    quiz = create_quiz(params)
    BATON.object = quiz
    return render_template('quiz_multiple_choice.html', quiz=quiz, form=form,
                           title='Multiple Choice Quiz', emoji=resolve_icon('question'))


@app.route('/quiz_results')
def quiz_results():
    return render_template('quiz_results.html', quiz=BATON.object,
                           title='Quiz Results', emoji=resolve_icon('question'))
