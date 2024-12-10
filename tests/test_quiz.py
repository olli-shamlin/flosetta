import pytest

from app.quiz import create_quiz
from app.quiz import Parameters
from app.quiz import Option
from app.quiz import CharacterOption
from app.quiz import TableOption
from app.quiz import WordOption
from app.quiz import QuizTypeOption
from app.quiz import MultipleChoiceSizeOption
from app.corpora import Character
from app.corpora import Word


class TestQuiz:

    def test_multiple_choice_quiz_basic(self) -> None:

        params = Parameters(**{'kind': Option.option_name(QuizTypeOption.MULTIPLE_CHOICE),
                               'table': Option.option_name(TableOption.SYLLABARY),
                               'prompt': Option.option_name(CharacterOption.ROMAJI),
                               'choice': Option.option_name(CharacterOption.HIRAGANA),
                               'size': 5})

        quiz = create_quiz(params)

        assert len(quiz.questions) == params.size
        for next_question in quiz.questions:
            assert len(next_question.elements) == 5
            assert all([isinstance(next_element, Character) for next_element in next_question.elements])

        return

    def test_match_quiz_basic(self) -> None:

        params = Parameters(**{'kind': Option.option_name(QuizTypeOption.MATCH),
                               'table': Option.option_name(TableOption.VOCABULARY),
                               'prompt': Option.option_name(WordOption.ENGLISH),
                               'choice': Option.option_name(WordOption.KANA),
                               'size': 5})

        quiz = create_quiz(params)

        assert len(quiz.questions) == params.size
        for next_question in quiz.questions:
            assert len(next_question.elements) == 5
            assert all([isinstance(next_element, Word) for next_element in next_question.elements])

        return

    def test_mega_match_quiz_basic(self) -> None:

        params = Parameters(**{'kind': Option.option_name(QuizTypeOption.MEGA_MATCH),
                               'table': Option.option_name(TableOption.SYLLABARY),
                               'prompt': Option.option_name(CharacterOption.HIRAGANA),
                               'choice': Option.option_name(CharacterOption.KATAKANA),
                               'size': 4})

        with pytest.raises(NotImplementedError):
            quiz = create_quiz(params)

        # assert len(quiz.questions) == 1
        # assert len(quiz.questions[0].elements) == (params.size ** 2) / 2
        # assert all([isinstance(e, Character) for e in quiz.questions[0].elements])

        return

    def test_table_quiz_basic(self) -> None:

        params = Parameters(**{'kind': Option.option_name(QuizTypeOption.KANA_TABLE),
                               'table': Option.option_name(TableOption.SYLLABARY),
                               'prompt': Option.option_name(CharacterOption.HIRAGANA),
                               'choice': Option.option_name(CharacterOption.KATAKANA),
                               'size': 1})

        with pytest.raises(NotImplementedError):
            quiz = create_quiz(params)

        # assert len(quiz.questions) == 1
        # assert len(quiz.questions[0].elements) == 13
        # assert all([isinstance(e, Character) for e in quiz.questions[0].elements])

        return

    def test_fill_in_the_blank_quiz_basic(self) -> None:

        params = Parameters(**{'kind': Option.option_name(QuizTypeOption.FILL_IN_THE_BLANK),
                               'table': Option.option_name(TableOption.SYLLABARY),
                               'prompt': Option.option_name(CharacterOption.HIRAGANA),
                               'choice': Option.option_name(CharacterOption.KATAKANA),
                               'size': 5})

        with pytest.raises(NotImplementedError):
            quiz = create_quiz(params)

        # assert len(quiz.questions) == params.size
        # for next_question in quiz.questions:
        #     assert (len(next_question.elements) == 1) and isinstance(next_question.elements[0], Character)

        return
