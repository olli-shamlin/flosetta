
from app.model import create_quiz
from app.model import QuizParameters
from app.model import MultipleChoiceItem


def test_quiz_setup_vocabulary():

    params = QuizParameters()
    params.table = 'Vocabulary'
    params.type_of_quiz = 'Multiple Choice'
    params.number_of_items = 5
    params.prompt_type = 'Kana'
    params.choice_type = 'English'

    quiz = create_quiz(params)

    assert len(quiz.items) == 5
    for item in quiz.items:
        assert isinstance(item, MultipleChoiceItem)

    return


def test_quiz_setup_syllabary():

    params = QuizParameters()
    params.table = 'Kana'
    params.type_of_quiz = 'Multiple Choice'
    params.number_of_items = 5
    params.prompt_type = 'Romaji'
    params.choice_type = 'Hiragana'

    quiz = create_quiz(params)

    assert len(quiz.items) == 5
    for item in quiz.items:
        assert isinstance(item, MultipleChoiceItem)

    return
