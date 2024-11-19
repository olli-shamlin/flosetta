
from app.model import create_quiz
from app.model import Parameters
from app.model import MultipleChoiceItem


def test_quiz_setup_vocabulary():

    params = Parameters()
    params.table = 'Vocabulary'
    params.kind = 'Multiple Choice'
    params.size = '5'
    params.prompt_type = 'Kana'
    params.choice_type = 'English'

    quiz = create_quiz(params)

    assert len(quiz.items) == 5
    for item in quiz.items:
        assert isinstance(item, MultipleChoiceItem)

    return


def test_quiz_setup_syllabary():

    params = Parameters()
    params.table = 'Syllabary'
    params.kind = 'Multiple Choice'
    params.size = '5'
    params.prompt_type = 'Romaji'
    params.choice_type = 'Hiragana'

    quiz = create_quiz(params)

    assert len(quiz.items) == 5
    for item in quiz.items:
        assert isinstance(item, MultipleChoiceItem)

    return
