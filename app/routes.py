
from app import app
from app.model import Vocabulary
from ._utils import resolve_icon, kana_reference_tables
from flask import render_template


@app.route('/')
@app.route('/index')
@app.route('/vocab')
def index():
    words = [w for w in Vocabulary().values()]
    return render_template('vocabulary.html',
                           words=words,
                           title='Vocabulary',
                           emoji=resolve_icon('backpack'))


@app.route('/kana')
def kana():
    return render_template('kana.html', reftabs=kana_reference_tables(), title='Kana', emoji=resolve_icon('brilliance'))
