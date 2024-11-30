# Test cases for each type of option
#
#   - enum is defined as expected; it only defines members for the required values
#   - cast from member to str
#   - cast from str to member
#   - all members' str values as a list
#
# Quiz parameter option values
#
# 1. Tables: 'Vocabulary', 'Syllabary'
# 2. Kinds of quizzes: 'Multiple Choice', 'Match', 'Mega Match', 'Kana Table'
# 3. Prompt & Choice:
#    a. for 'Vocabulary' table: 'English', 'Romaji', 'Kana', 'Kanji'
#    b. for 'Syllabary' table: 'Romaji', 'Hiragana', 'Katakana'
# 4. Size
#    a. for 'Multiple Choice' and 'Match' kinds of quizzes: 5, 10, 15, 20
#    b. for 'Mega Match' kind of quiz: 4, 6, 8

from app.quiz import TableOption
from app.quiz import QuizTypeOption
from app.quiz import WordOption
from app.quiz import CharacterOption
from app.quiz import MatchSizeOption
from app.quiz import MegaMatchSizeOption
from app.quiz import MultipleChoiceSizeOption


class TestQuizOptions:

    def test_table_option(self) -> None:

        expected_values = {
            'Vocabulary': TableOption.VOCABULARY,
            'Syllabary': TableOption.SYLLABARY
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(TableOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        assert set(TableOption.valid_values()) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert TableOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert TableOption.option_name(as_member) == as_str

        return

    def test_quiz_type_option(self) -> None:

        expected_values = {
            'Match': QuizTypeOption.MATCH,
            'Multiple Choice': QuizTypeOption.MULTIPLE_CHOICE,
            'Mega Match': QuizTypeOption.MEGA_MATCH,
            'Kana Table': QuizTypeOption.KANA_TABLE,
            'Fill In The Blank': QuizTypeOption.FILL_IN_THE_BLANK
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(QuizTypeOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        assert set(QuizTypeOption.valid_values()) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert QuizTypeOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert QuizTypeOption.option_name(as_member) == as_str

        return

    def test_word_option(self) -> None:

        expected_values = {
            'Romaji': WordOption.ROMAJI,
            'Kana': WordOption.KANA,
            'Kanji': WordOption.KANJI,
            'English': WordOption.ENGLISH,
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(WordOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        assert set(WordOption.valid_values()) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert WordOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert WordOption.option_name(as_member) == as_str

        return

    def test_character_option(self) -> None:

        expected_values = {
            'Romaji': CharacterOption.ROMAJI,
            'Hiragana': CharacterOption.HIRAGANA,
            'Katakana': CharacterOption.KATAKANA,
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(CharacterOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        assert set(CharacterOption.valid_values()) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert CharacterOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert CharacterOption.option_name(as_member) == as_str

        return

    def test_multiple_choice_size_option(self) -> None:

        expected_values = {
            '5': MultipleChoiceSizeOption.FIVE,
            '10': MultipleChoiceSizeOption.TEN,
            '15': MultipleChoiceSizeOption.FIFTEEN,
            '20': MultipleChoiceSizeOption.TWENTY,
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(MultipleChoiceSizeOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        vals = MultipleChoiceSizeOption.valid_values()
        assert set(vals) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert MultipleChoiceSizeOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert MultipleChoiceSizeOption.option_name(as_member) == as_str

        return

    def test_match_size_option(self) -> None:

        expected_values = {
            '5': MatchSizeOption.FIVE,
            '10': MatchSizeOption.TEN,
            '15': MatchSizeOption.FIFTEEN,
            '20': MatchSizeOption.TWENTY,
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(MatchSizeOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        vals = MatchSizeOption.valid_values()
        assert set(vals) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert MatchSizeOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert MatchSizeOption.option_name(as_member) == as_str

        return

    def test_mega_match_size_option(self) -> None:

        expected_values = {
            '4': MegaMatchSizeOption.FOUR,
            '6': MegaMatchSizeOption.SIX,
            '8': MegaMatchSizeOption.EIGHT,
        }

        # Check 1: the number of enum members is the same as the number of expected values
        assert len(MegaMatchSizeOption) == len(expected_values)

        # Check 2: the enum member names match the expected values
        vals = MegaMatchSizeOption.valid_values()
        assert set(vals) == set(expected_values.keys())

        for as_str, as_member in expected_values.items():

            # Check 3: string representations of values are correctly coerced to member values
            assert MegaMatchSizeOption.to_member(as_str) == as_member

            # Check 4: member values are correctly coerced to string representations
            assert MegaMatchSizeOption.option_name(as_member) == as_str

        return
