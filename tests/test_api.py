import enum

import app

import inspect
import pytest


@pytest.fixture
def expected_modules() -> set[str]:
    # TODO OBSOLETE QUIZ: return {'corpora', 'data_paths', 'flogger', 'forms', 'logging', 'model', 'routes', 'utils'}
    return {'corpora', 'data_paths', 'flogger', 'forms', 'logging', 'routes', 'utils', 'quiz'}


def _is_class(obj): return lambda obj: inspect.isclass(obj)
def _is_dict(obj): return lambda obj: isinstance(obj, dict)
def _is_function(obj): return lambda obj: inspect.isfunction(obj)
def _is_int(obj): return lambda obj: isinstance(obj, int)
def _is_module(obj): return lambda obj: inspect.ismodule(obj)
def _is_str(obj): return lambda obj: isinstance(obj, str)


def get_app_modules():
    members = inspect.getmembers(app)
    as_dict = {member[0]: member[1] for member in members}
    filtered = {name: member for name, member in as_dict.items() if inspect.ismodule(member) and name != 'inspect'}
    return filtered


def get_module_members(module_name: str) -> list[tuple]:
    """Get the list of module members.

    Items of the returned list are tuples. The first item in each tuple is the member's name;
    the second item is the member's type.
    """
    modules = get_app_modules()
    # TODO can the if clause in the following be moved to the inspect.getmembers call above?
    # TODO See doc re inspect.getmember's predicate param
    return [member for member in inspect.getmembers(modules[module_name])
            if not (member[0].startswith('__') and member[0].endswith('__'))]


class TestAPI:

    def test_modules(self, expected_modules) -> None:
        """Verify the set of modules in the is stable."""
        modules = get_app_modules()
        module_names = {name for name in modules.keys()}

        assert module_names == expected_modules

        return

    def test_corpora(self) -> None:

        expected_members = {
            'Character': _is_class,
            'Corpus': _is_class,
            'CorpusType': lambda obj: str(obj) == "<enum 'CorpusType'>",
            'Element': _is_class,
            'Metrics': _is_class,
            'Word': _is_class,
            '_CACHE': _is_dict,
            '_ELEMENT_FACTORY': _is_dict,
            '_Enum': lambda obj: isinstance(obj, enum.EnumMeta),
            '_LOADER': _is_dict,
            '_Optional': lambda obj: str(type(obj)) == "<class 'typing._SpecialForm'>",
            '_asdict': _is_function,
            '_character_factory': _is_function,
            '_dataclass': _is_function,
            '_date': _is_class,
            '_load_syllabary': _is_function,
            '_load_vocabulary': _is_function,
            '_save_metrics': _is_function,
            '_store': _is_module,
            '_word_factory': _is_function,
            'character_store_key': _is_function,
            'fetch': _is_function,
            'flush': _is_function,
            'word_store_key': _is_function
        }

        members = get_module_members('corpora')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return

    def test_data_paths(self) -> None:

        expected_members = {
            'QUIZ_ITEMS_FILE': _is_str,
            'SYLLABARY_FILE': _is_str,
            'SYLLABARY_METRICS_FILE': _is_str,
            'VOCABULARY_FILE': _is_str,
            'VOCABULARY_METRICS_FILE': _is_str,
            '_APP_DATA_PATH': _is_str,
            '_APP_INSTALL_PATH': _is_str,
            '_APP_STATIC_PATH': _is_str,
            '_APP_TEST_PATH': _is_str,
            '_FLEX_PATH': _is_str,
            '_JAVASCRIPT_EXT': _is_str,
            '_JSON_EXT': _is_str,
            '_SPREADSHEET_EXT': _is_str,
            '_SYLLABARY_NAME': _is_str,
            '_VOCABULARY_NAME': _is_str,
            'os': _is_module,
            'app': lambda obj: str(obj) == "<Flask 'app'>",
        }

        members = get_module_members('data_paths')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return

    def test_flogger(self) -> None:

        expected_members = {
            'DEBUG': _is_int,
            'ERROR': _is_int,
            'INFO': _is_int,
            'WARN': _is_int,
            'WARNING': _is_int,
            '_AppLog': _is_class,
            'app': lambda obj: str(obj) == "<Flask 'app'>",
            'inspect': _is_module,
            'tracer': _is_function,
            'flogger': lambda obj: str(type(obj)) == '<class \'app.flogger._AppLog\'>',
        }

        members = get_module_members('flogger')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return

    def test_forms(self) -> None:

        expected_members = {
            'FlaskForm': _is_class,
            'HiddenInput': _is_class,
            'MultipleChoiceQuizForm': _is_class,
            'QuizSetupForm1': _is_class,
            'QuizSetupForm2a': _is_class,
            'QuizSetupForm2b': _is_class,
            'QuizSetupForm3': _is_class,
            'QuizSetupForm4': _is_class,
            'QuizSetupForm5': _is_class,
            'QuizSetupForm6': _is_class,
            'RadioField': _is_class,
            'StringField': _is_class,
            'SubmitField': _is_class,
        }

        members = get_module_members('forms')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return

    def test_logging(self) -> None:

        expected_members = {
            'DEBUG': _is_int,
            'ERROR': _is_int,
            'INFO': _is_int,
            'WARN': _is_int,
            'WARNING': _is_int,
            '_AppLog': _is_class,
            'app': lambda obj: str(obj) == "<Flask 'app'>",
            'flogger': lambda obj: str(type(obj)) == '<class \'app.flogger._AppLog\'>',
            'inspect': _is_module,
            'tracer': _is_function,
        }

        members = get_module_members('flogger')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return

    def test_routes(self) -> None:

        expected_members = {
            'BATON': _is_class,
            'Corpus': _is_class,
            'CorpusType': lambda obj: str(obj) == "<enum 'CorpusType'>",
            'MultipleChoiceQuizForm': _is_class,
            'Parameters': _is_class,
            'QuizSetupForm1': _is_class,
            'QuizSetupForm2a': _is_class,
            'QuizSetupForm2b': _is_class,
            'QuizSetupForm3': _is_class,
            'QuizSetupForm4': _is_class,
            'QuizSetupForm5': _is_class,
            'QuizSetupForm6': _is_class,
            'TableOption': _is_class,
            'app': lambda obj: str(obj) == "<Flask 'app'>",
            'create_quiz': _is_function,
            'index': _is_function,
            'kana': _is_function,
            'kana_reference_tables': _is_function,
            'multiple_choice_quiz': _is_function,
            'quiz_results': _is_function,
            'quiz_setup': _is_function,
            'quiz_setup2': _is_function,
            'quiz_setup3': _is_function,
            'quiz_setup4': _is_function,
            'quiz_setup5': _is_function,
            'quiz_setup6': _is_function,
            'redirect': _is_function,
            'render_template': _is_function,
            'request': _is_function,
            'resolve_icon': _is_function,
        }

        members = get_module_members('routes')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return

    def test_utils(self) -> None:

        expected_members = {
            'BATON': _is_class,
            'Corpus': _is_class,
            'CorpusType': _is_class,
            'Markup': _is_class,
            '_PassTheBaton': _is_class,
            'kana_reference_tables': _is_function,
            'resolve_icon': _is_function,
        }

        members = get_module_members('utils')
        assert {member[0] for member in members} == {k for k in expected_members.keys()}

        for member_name, member_inst in members:
            assert member_name in expected_members.keys()
            assert member_name and expected_members[member_name](member_inst)

        return
