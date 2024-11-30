
from app.quiz import create_quiz
from app.quiz import Parameters
from app.quiz import CharacterOption
from app.quiz import TableOption
from app.quiz import WordOption
from app.quiz import QuizTypeOption
from app.corpora import Character
from app.corpora import Word


class TestQuiz:

    def test_multiple_choice_quiz_basic(self) -> None:

        params = Parameters()
        params.table = TableOption.SYLLABARY
        params.kind = QuizTypeOption.MULTIPLE_CHOICE
        params.size = 5
        params.prompt_type = CharacterOption.ROMAJI
        params.choice_type = CharacterOption.HIRAGANA

        quiz = create_quiz(params)

        assert len(quiz.questions) == params.size
        for next_question in quiz.questions:
            assert len(next_question.elements) == 5
            assert all([isinstance(next_element, Character) for next_element in next_question.elements])

        return

    def test_match_quiz_basic(self) -> None:

        params = Parameters()
        params.table = TableOption.VOCABULARY
        params.kind = QuizTypeOption.MATCH
        params.size = 5
        params.prompt_type = WordOption.ENGLISH
        params.choice_type = WordOption.KANA

        quiz = create_quiz(params)

        assert len(quiz.questions) == params.size
        for next_question in quiz.questions:
            assert len(next_question.elements) == 5
            assert all([isinstance(next_element, Word) for next_element in next_question.elements])

        return

    def test_mega_match_quiz_basic(self) -> None:

        params = Parameters()
        params.table = TableOption.SYLLABARY
        params.kind = QuizTypeOption.MEGA_MATCH
        params.size = 4
        params.prompt_type = CharacterOption.HIRAGANA
        params.choice_type = CharacterOption.KATAKANA

        quiz = create_quiz(params)

        assert len(quiz.questions) == 1
        assert len(quiz.questions[0].elements) == (params.size ** 2) / 2
        assert all([isinstance(e, Character) for e in quiz.questions[0].elements])

        return

    def test_table_quiz_basic(self) -> None:

        params = Parameters()
        params.table = TableOption.SYLLABARY
        params.kind = QuizTypeOption.KANA_TABLE
        params.prompt_type = CharacterOption.HIRAGANA

        quiz = create_quiz(params)

        assert len(quiz.questions) == 1
        assert len(quiz.questions[0].elements) == 13
        assert all([isinstance(e, Character) for e in quiz.questions[0].elements])

        return

    def test_fill_in_the_blank_quiz_basic(self) -> None:

        params = Parameters()
        params.table = TableOption.SYLLABARY
        params.kind = QuizTypeOption.FILL_IN_THE_BLANK
        params.size = 5
        params.prompt_type = CharacterOption.HIRAGANA

        quiz = create_quiz(params)

        assert len(quiz.questions) == params.size
        for next_question in quiz.questions:
            assert (len(next_question.elements) == 1) and isinstance(next_question.elements[0], Character)

        return
