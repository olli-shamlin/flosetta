
from . import app
from .forms import QuizSetupForm1
from .forms import QuizSetupForm2a
from .forms import QuizSetupForm2b
from .forms import QuizSetupForm3
from .forms import QuizSetupForm4
from .forms import QuizSetupForm5
from .forms import QuizSetupForm6
from .forms import MultipleChoiceQuizForm
# TODO OBSOLETE CORPORA: from .model import Vocabulary
from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora._store.serializer import json_decoder
# TODO OBSOLETE QUIZ: from .model import Parameters
# TODO OBSOLETE QUIZ: from .model import TableOption
# TODO OBSOLETE QUIZ: from .model import create_quiz
from .quiz import Parameters
from .quiz import TableOption
from .quiz import QuizTypeOption
from .quiz import WordOption
from .quiz import MultipleChoiceSizeOption
from .quiz import create_quiz
from .utils import resolve_icon
from .utils import kana_reference_tables
from .utils import BATON

from flask import redirect
from flask import render_template
from flask import request


@app.route('/')
@app.route('/index')
@app.route('/vocab')
def index():
    # TODO OBSOLETE CORPORA: vocabulary = Vocabulary()
    vocabulary = Corpus(CorpusType.VOCABULARY)
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
        BATON.object = quiz.process_results(json_decoder(str(form.responses.data)))
        return redirect('/quiz_results')
    params = BATON.object
    quiz = create_quiz(params)
    form.responses.data = quiz.transport
    BATON.object = quiz
    return render_template('quiz_multiple_choice.html', quiz=quiz, form=form,
                           title='Multiple Choice Quiz', emoji=resolve_icon('question'))


@app.route('/quiz_results')
def quiz_results():
    quiz_summary = BATON.object
    return render_template('quiz_results.html', summary=quiz_summary,
                           title='Quiz Results', emoji=resolve_icon('question'))


@app.route('/proto', methods=['GET', 'POST'])
def proto_route():
    form = MultipleChoiceQuizForm()
    if form.validate_on_submit():
        pass
    params = Parameters()
    params.table = TableOption.VOCABULARY
    params.kind = QuizTypeOption.MULTIPLE_CHOICE
    params.size = MultipleChoiceSizeOption.FIVE
    params.prompt_type = WordOption.ENGLISH
    params.choice_type = WordOption.KANA
    quiz = create_quiz(params)
    form.responses.data = quiz.transport
    return render_template('quiz_multiple_choice.html', quiz=quiz, form=form,
                           title='Multiple Choice Quiz', emoji=resolve_icon('question'))
