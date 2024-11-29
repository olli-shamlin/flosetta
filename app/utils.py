
from markupsafe import Markup
from app import app
# TODO OBSOLETE CORPORA: from app.model import Syllabary
from app.corpora import Corpus
from app.corpora import CorpusType


def resolve_icon(name: str) -> str:

    icon_map = {
        'robot': Markup('xmlns="http://www.w3.org/2000/svg" width="40" height="32" fill="currentColor" '
                        'class="bi bi-robot" viewBox="0 0 16 16">'
                        '<path d="M6 12.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M3 8.062C3 '
                        '6.76 4.235 5.765 5.53 5.886a26.6 26.6 0 0 0 4.94 0C11.765 5.765 13 6.76 13 8.062v1.157a.93.93 '
                        '0 0 1-.765.935c-.845.147-2.34.346-4.235.346s-3.39-.2-4.235-.346A.93.93 0 0 1 3 9.219zm4.542-.'
                        '827a.25.25 0 0 0-.217.068l-.92.9a25 25 0 0 1-1.871-.183.25.25 0 0 0-.068.495c.55.076 1.232.'
                        '149 2.02.193a.25.25 0 0 0 .189-.071l.754-.736.847 1.71a.25.25 0 0 0 .404.062l.932-.97a25 '
                        '25 0 0 0 1.922-.188.25.25 0 0 0-.068-.495c-.538.074-1.207.145-1.98.189a.25.25 0 0 0-.166.'
                        '076l-.754.785-.842-1.7a.25.25 0 0 0-.182-.135"/><path d="M8.5 1.866a1 1 0 1 0-1 0V3h-2A4.5 '
                        '4.5 0 0 0 1 7.5V8a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1v1a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-1a1 1 0 0 0 '
                        '1-1V9a1 1 0 0 0-1-1v-.5A4.5 4.5 0 0 0 10.5 3h-2zM14 7.5V13a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7.'
                        '5A3.5 3.5 0 0 1 5.5 4h5A3.5 3.5 0 0 1 14 7.5"'),
        'backpack': Markup('xmlns="http://www.w3.org/2000/svg" width="40" height="32" fill="currentColor" '
                           'class="bi bi-backpack3" viewBox="0 0 16 16">'
                           '<path d="M4.04 7.43a4 4 0 0 1 7.92 0 .5.5 0 1 1-.99.14 3 3 0 0 0-5.94 0 .5.5 0 1 1-.99-.'
                           '14M4 9.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 .5.5v4a.5.5 0 0 1-.5.5h-7a.5.5 0 0 1-.5-.5zm1 .'
                           '5v3h6v-3h-1v.5a.5.5 0 0 1-1 0V10z"/><path d="M6 2.341V2a2 2 0 1 1 4 0v.341c.465.165.904.'
                           '385 1.308.653l.416-1.247a1 1 0 0 1 1.748-.284l.77 1.027a1 1 0 0 1 .15.917l-.803 2.407C13.'
                           '854 6.49 14 7.229 14 8v5.5a2.5 2.5 0 0 1-2.5 2.5h-7A2.5 2.5 0 0 1 2 13.5V8c0-.771.146-1.'
                           '509.41-2.186l-.802-2.407a1 1 0 0 1 .15-.917l.77-1.027a1 1 0 0 1 1.748.284l.416 1.247A6 '
                           '6 0 0 1 6 2.34ZM7 2v.083a6 6 0 0 1 2 0V2a1 1 0 1 0-2 0m5.941 2.595.502-1.505-.77-1.027-.'
                           '532 1.595q.447.427.8.937M3.86 3.658l-.532-1.595-.77 1.027.502 1.505q.352-.51.8-.937M8 3a5 '
                           '5 0 0 0-5 5v5.5A1.5 1.5 0 0 0 4.5 15h7a1.5 1.5 0 0 0 1.5-1.5V8a5 5 0 0 0-5-5"'),
        'brilliance': Markup('xmlns="http://www.w3.org/2000/svg" width="40" height="32" fill="currentColor" '
                             'class="bi bi-brilliance" viewBox="0 0 16 16"><path d="M8 16A8 8 0 1 1 8 0a8 8 0 0 1 0 '
                             '16M1 8a7 7 0 0 0 7 7 3.5 3.5 0 1 0 0-7 3.5 3.5 0 1 1 0-7 7 7 0 0 0-7 7"/>'),
        'speedometer2': Markup('xmlns="http://www.w3.org/2000/svg" width="40" height="32" fill="currentColor" '
                               'class="bi bi-speedometer2" viewBox="0 0 16 16">'
                               '<path d="M8 4a.5.5 0 0 1 .5.5V6a.5.5 0 0 1-1 0V4.5A.5.5 0 0 1 8 4M3.732 5.732a.5.5 0 0 '
                               '1 .707 0l.915.914a.5.5 0 1 1-.708.708l-.914-.915a.5.5 0 0 1 0-.707M2 10a.5.5 0 0 1 '
                               '.5-.5h1.586a.5.5 0 0 1 0 1H2.5A.5.5 0 0 1 2 10m9.5 0a.5.5 0 0 1 .5-.5h1.5a.5.5 0 0 1 0 '
                               '1H12a.5.5 0 0 1-.5-.5m.754-4.246a.39.39 0 0 0-.527-.02L7.547 9.31a.91.91 0 1 0 1.302 '
                               '1.258l3.434-4.297a.39.39 0 0 0-.029-.518z"/><path fill-rule="evenodd" d="M0 10a8 8 0 1 '
                               '1 15.547 2.661c-.442 1.253-1.845 1.602-2.932 1.25C11.309 13.488 9.475 13 8 13c-1.474 '
                               '0-3.31.488-4.615.911-1.087.352-2.49.003-2.932-1.25A8 8 0 0 1 0 10m8-7a7 7 0 0 0-6.603 '
                               '9.329c.203.575.923.876 1.68.63C4.397 12.533 6.358 12 8 12s3.604.532 4.923.96c.757.245 '
                               '1.477-.056 1.68-.631A7 7 0 0 0 8 3"/>'),
        'question': Markup('xmlns="http://www.w3.org/2000/svg" width="40" height="32" fill="currentColor" '
                           'class="bi bi-question-octagon" viewBox="0 0 16 16"><path d="M4.54.146A.5.5 0 0 1 '
                           '4.893 0h6.214a.5.5 0 0 1 .353.146l4.394 4.394a.5.5 0 0 1 .146.353v6.214a.5.5 0 0 '
                           '1-.146.353l-4.394 4.394a.5.5 0 0 1-.353.146H4.893a.5.5 0 0 1-.353-.146L.146 '
                           '11.46A.5.5 0 0 1 0 11.107V4.893a.5.5 0 0 1 .146-.353zM5.1 1 1 5.1v5.8L5.1 15h5.'
                           '8l4.1-4.1V5.1L10.9 1z"/><path d="M5.255 5.786a.237.237 0 0 0 .241.247h.825c.138 0 '
                           '.248-.113.266-.25.09-.656.54-1.134 1.342-1.134.686 0 1.314.343 1.314 1.168 0 '
                           '.635-.374.927-.965 1.371-.673.489-1.206 1.06-1.168 1.987l.003.217a.25.25 0 0 0 '
                           '.25.246h.811a.25.25 0 0 0 .25-.25v-.105c0-.718.273-.927 1.01-1.486.609-.463 '
                           '1.244-.977 1.244-2.056 0-1.511-1.276-2.241-2.673-2.241-1.267 0-2.655.59-2.75 '
                           '2.286m1.557 5.763c0 .533.425.927 1.01.927.609 0 1.028-.394 1.028-.927 0-.552-.42-'
                           '.94-1.029-.94-.584 0-1.009.388-1.009.94"/>'),
    }

    assert name in icon_map.keys()
    return icon_map[name]


def kana_reference_tables():

    # TODO OBSOLETE CORPORA: m = Syllabary()
    corpus = Corpus(CorpusType.SYLLABARY)
    m = {character.romaji: character for character in corpus}

    tables = {
        'Basic': {
            ' ':   {'a': m['a'],   'i': m['i'],    'u': m['u'],   'e': m['e'],  'o': m['o']},
            'k':   {'a': m['ka'],  'i': m['ki'],   'u': m['ku'],  'e': m['ke'], 'o': m['ko']},
            's':   {'a': m['sa'],  'i': m['shi'],  'u': m['su'],  'e': m['se'], 'o': m['so']},
            't':   {'a': m['ta'],  'i': m['chi'],  'u': m['tsu'], 'e': m['te'], 'o': m['to']},
            'n':   {'a': m['na'],  'i': m['ni'],   'u': m['nu'],  'e': m['ne'], 'o': m['no']},
            'h':   {'a': m['ha'],  'i': m['hi'],   'u': m['fu'],  'e': m['he'], 'o': m['ho']},
            'm':   {'a': m['ma'],  'i': m['mi'],   'u': m['mu'],  'e': m['me'], 'o': m['mo']},
            'y':   {'a': m['ya'],  'i': None,      'u': m['yu'],  'e': None,    'o': m['yo']},
            'r':   {'a': m['ra'],  'i': m['ri'],   'u': m['ru'],  'e': m['re'], 'o': m['ro']},
            'w':   {'a': m['wa'],  'i': None,      'u': None,     'e': None,    'o': m['wo']},
            'n/m': {'a': m['n/m'], 'i': None,      'u': None,     'e': None,    'o': None},
        },
        'Dakuten': {
            'g': {'a': m['ga'], 'i': m['gi'],  'u': m['gu'],  'e': m['ge'], 'o': m['go']},
            'z': {'a': m['za'], 'i': m['ji'],  'u': m['zu'],  'e': m['ze'], 'o': m['zo']},
            'd': {'a': m['da'], 'i': m['dzi'], 'u': m['dzu'], 'e': m['de'], 'o': m['do']},
            'b': {'a': m['ba'], 'i': m['bi'],  'u': m['bu'],  'e': m['be'], 'o': m['bo']},
            'p': {'a': m['pa'], 'i': m['pi'],  'u': m['pu'],  'e': m['pe'], 'o': m['po']},
        },
        'Modified': {
            'ky': {'a': m['kya'], 'u': m['kyu'], 'o': m['kyo']},
            'gy': {'a': m['gya'], 'u': m['gyu'], 'o': m['gyo']},
            'sh': {'a': m['sha'], 'u': m['shu'], 'o': m['sho']},
            'jy':  {'a': m['jya'], 'u': m['jyu'], 'o': m['jyo']},
            'ch': {'a': m['cha'], 'u': m['chu'], 'o': m['cho']},
            'ny': {'a': m['nya'], 'u': m['nyu'], 'o': m['nyo']},
            'hy': {'a': m['hya'], 'u': m['hyu'], 'o': m['hyo']},
            'by': {'a': m['bya'], 'u': m['byu'], 'o': m['byo']},
            'my': {'a': m['mya'], 'u': m['myu'], 'o': m['myo']},
            'py': {'a': m['pya'], 'u': m['pyu'], 'o': m['pyo']},
            'ry': {'a': m['rya'], 'u': m['ryu'], 'o': m['ryo']},
        },
    }

    return tables


class _PassTheBaton:

    _object = None

    @property
    def object(self):
        assert _PassTheBaton._object is not None
        o = _PassTheBaton._object
        _PassTheBaton._object = None
        return o

    @object.setter
    def object(self, obj):
        assert _PassTheBaton._object is None
        _PassTheBaton._object = obj
        return

    def drop(self) -> None:
        _PassTheBaton._object = None


BATON = _PassTheBaton()
