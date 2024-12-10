
from . import app
from .forms import QuizSetupForm
from .forms import QuizForm
from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora._store.serializer import json_decoder
from .quiz import Parameters
from .quiz import create_quiz
from .utils import resolve_icon
from .utils import kana_reference_tables
from .utils import BATON

from flask import redirect
from flask import render_template


@app.route('/')
@app.route('/index')
@app.route('/vocab')
def index():
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
    form = QuizSetupForm()
    if form.validate_on_submit():
        t = json_decoder(str(form.transport.data))
        BATON.object = create_quiz(Parameters(**t))
        return redirect('/quiz')
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz', methods=['GET', 'POST'])
def execute_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        quiz = BATON.object
        BATON.object = quiz.process_results(json_decoder((str(form.transport.data))))
        return redirect('/quiz_results')
    quiz = BATON.object
    form.transport.data = quiz.transport
    BATON.object = quiz
    return render_template(quiz.html_template, quiz=quiz, form=form, title=quiz.name, emoji=resolve_icon('question'))


@app.route('/quiz_results')
def quiz_results():
    quiz_summary = BATON.object
    return render_template('quiz_results.html', summary=quiz_summary,
                           title='Quiz Results', emoji=resolve_icon('question'))
#
#
# @app.route('/proto', methods=['GET', 'POST'])
# def proto_route():
#     form = MultipleChoiceQuizForm()
#     if form.validate_on_submit():
#         pass
#     params = Parameters()
#     params.table = TableOption.VOCABULARY
#     params.kind = QuizTypeOption.MULTIPLE_CHOICE
#     params.size = MultipleChoiceSizeOption.FIVE
#     params.prompt_type = WordOption.ENGLISH
#     params.choice_type = WordOption.KANA
#     quiz = create_quiz(params)
#     form.responses.data = quiz.transport
#     return render_template('quiz_multiple_choice.html', quiz=quiz, form=form,
#                            title='Multiple Choice Quiz', emoji=resolve_icon('question'))
