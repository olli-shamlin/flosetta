
# TODO OBSOLETE QUIZ from app.model import create_quiz
# TODO OBSOLETE QUIZ from app.model import Parameters
# TODO OBSOLETE QUIZ from app.model import MultipleChoiceItem
# TODO OBSOLETE QUIZ from app.model import CharacterItem
# TODO OBSOLETE QUIZ from app.model import WordItem
from app.quiz import create_quiz
from app.quiz import Parameters
from app.quiz import MultipleChoiceItem
# from app.quiz import CharacterItem
# from app.quiz import WordItem


class TestMultipleChoiceQuiz:

    def test_quiz_setup_vocabulary(self) -> None:

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

    def test_quiz_setup_syllabary(self) -> None:

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
