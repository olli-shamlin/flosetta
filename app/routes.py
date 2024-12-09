
from . import app
from .forms import QuizSetupForm1
from .forms import QuizSetupForm2a
from .forms import QuizSetupForm2b
from .forms import QuizSetupForm3
from .forms import QuizSetupForm4
from .forms import QuizSetupForm5
from .forms import QuizSetupForm6
# TODO OBSOLETE from .forms import MultipleChoiceQuizForm
from .forms import QuizForm
from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora._store.serializer import json_decoder
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
    form.choice_type.choices = params.choice_options
    BATON.object = params
    return render_template('quiz_setup.html', form=form, title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz_setup6', methods=['GET', 'POST'])
def quiz_setup6():
    form = QuizSetupForm6(request.form)
    if request.method == 'POST':
        if form.cancel.data:
            BATON.drop()
            return redirect('/index')
        return redirect('/quiz')
    params = BATON.object
    BATON.object = params
    return render_template('quiz_start.html', form=form, quiz_params=params,
                           title='Quiz Setup', emoji=resolve_icon('question'))


@app.route('/quiz', methods=['GET', 'POST'])
def execute_quiz():
    form = QuizForm()
    if form.validate_on_submit():
        quiz = BATON.object
        BATON.object = quiz.process_results(json_decoder((str(form.transport.data))))
        return redirect('/quiz_results')
    params = BATON.object
    quiz = create_quiz(params)
    form.transport.data = quiz.transport
    BATON.object = quiz
    return render_template(quiz.html_template, quiz=quiz, form=form, title=quiz.name, emoji=resolve_icon('question'))


# TODO OBSOLETE # @app.route('/multiple_choice_quiz', methods=['GET', 'POST'])
# TODO OBSOLETE # def multiple_choice_quiz():
# TODO OBSOLETE #     form = MultipleChoiceQuizForm()
# TODO OBSOLETE #     if form.validate_on_submit():
# TODO OBSOLETE #         quiz = BATON.object
# TODO OBSOLETE #         BATON.object = quiz.process_results(json_decoder(str(form.responses.data)))
# TODO OBSOLETE #         return redirect('/quiz_results')
# TODO OBSOLETE #     params = BATON.object
# TODO OBSOLETE #     quiz = create_quiz(params)
# TODO OBSOLETE #     form.responses.data = quiz.transport
# TODO OBSOLETE #     BATON.object = quiz
# TODO OBSOLETE #     return render_template('quiz_multiple_choice.html', quiz=quiz, form=form,
# TODO OBSOLETE #                            title='Multiple Choice Quiz', emoji=resolve_icon('question'))
# TODO OBSOLETE #
# TODO OBSOLETE #
# TODO OBSOLETE # @app.route('/match_quiz', methods=['GET', 'POST'])
# TODO OBSOLETE # def multiple_choice_quiz():
# TODO OBSOLETE #     form = MultipleChoiceQuizForm()
# TODO OBSOLETE #     if form.validate_on_submit():
# TODO OBSOLETE #         quiz = BATON.object
# TODO OBSOLETE #         BATON.object = quiz.process_results(json_decoder(str(form.responses.data)))
# TODO OBSOLETE #         return redirect('/quiz_results')
# TODO OBSOLETE #     params = BATON.object
# TODO OBSOLETE #     quiz = create_quiz(params)
# TODO OBSOLETE #     form.responses.data = quiz.transport
# TODO OBSOLETE #     BATON.object = quiz
# TODO OBSOLETE #     return render_template('quiz_match.html', quiz=quiz, form=form,
# TODO OBSOLETE #                            title='Match Quiz', emoji=resolve_icon('question'))
# TODO OBSOLETE #
# TODO OBSOLETE #
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
