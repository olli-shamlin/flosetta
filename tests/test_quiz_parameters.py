
from app.model import Parameters
from app.model import TableOption
from app.model import QuizTypeOption
from app.model import CharacterOption
from app.model import WordOption
from app.model import MatchSizeOption
from app.model import MegaMatchSizeOption
from app.model import MultipleChoiceSizeOption
from app.model import OptionValueError
from app.model import ParameterOrderError
import pytest


def test_table_option_bad_value():

    params = Parameters()
    with pytest.raises(OptionValueError) as excinfo:
        params.table = 'invalid'
    assert str(excinfo.value) == '"invalid" is an invalid value for TableOption'

    return


def test_table_option():

    params = Parameters()

    params.table = 'Syllabary'
    assert params.table == TableOption.SYLLABARY

    params.table = 'Vocabulary'
    assert params.table == TableOption.VOCABULARY

    return


def test_kind_option_order_constraint():

    params = Parameters()

    with pytest.raises(ParameterOrderError) as excinfo:
        params.kind = 'Multiple Choice'
    assert str(excinfo.value) == '"table" parameter must be set before "kind" parameter'

    return


def test_kind_option_bad_value():

    params = Parameters()

    params.table = 'Syllabary'
    with pytest.raises(OptionValueError) as excinfo:
        params.table = 'invalid'
    assert str(excinfo.value) == '"invalid" is an invalid value for TableOption'

    params.table = 'Vocabulary'
    with pytest.raises(OptionValueError) as excinfo:
        params.table = 'invalid'
    assert str(excinfo.value) == '"invalid" is an invalid value for TableOption'

    return


def test_kind_option_with_syllabary():

    params = Parameters()
    params.table = 'Syllabary'

    params.kind = 'Multiple Choice'
    assert params.kind == QuizTypeOption.MULTIPLE_CHOICE
    params.kind = 'Match'
    assert params.kind == QuizTypeOption.MATCH
    params.kind = 'Kana Table'
    assert params.kind == QuizTypeOption.KANA_TABLE
    params.kind = 'Mega Match'
    assert params.kind == QuizTypeOption.MEGA_MATCH

    return


def test_kind_option_with_vocabulary():

    params = Parameters()
    params.table = 'Vocabulary'

    # Only "multiple choice" and "match" quiz types are supported with the Vocabulary table
    params.kind = 'Multiple Choice'
    assert params.kind == QuizTypeOption.MULTIPLE_CHOICE
    params.kind = 'Match'
    assert params.kind == QuizTypeOption.MATCH
    with pytest.raises(OptionValueError) as excinfo:
        params.kind = 'Kana Table'
    assert str(excinfo.value) == '"Kana Table" is an invalid value for kind'
    with pytest.raises(OptionValueError) as excinfo:
        params.kind = 'Mega Match'
    assert str(excinfo.value) == '"Mega Match" is an invalid value for kind'

    return


def test_size_option_order_constraint():

    params = Parameters()

    with pytest.raises(ParameterOrderError) as excinfo:
        params.size = 5
    assert str(excinfo.value) == '"kind" parameter must be set before "size" parameter'

    return


def test_size_option_bad_value_with_vocabulary():

    params = Parameters()
    params.table = 'Vocabulary'

    params.kind = 'Match'
    with pytest.raises(OptionValueError) as excinfo:
        params.size = '1000'
    assert str(excinfo.value) == '"1000" is an invalid value for MatchSizeOption'

    params.kind = 'Multiple Choice'
    with pytest.raises(OptionValueError) as excinfo:
        params.size = '1000'
    assert str(excinfo.value) == '"1000" is an invalid value for MultipleChoiceSizeOption'

    return


def test_size_option_bad_value_with_syllabary():

    params = Parameters()
    params.table = 'Syllabary'

    params.kind = 'Match'
    with pytest.raises(OptionValueError) as excinfo:
        params.size = '1000'
    assert str(excinfo.value) == '"1000" is an invalid value for MatchSizeOption'

    params.kind = 'Multiple Choice'
    with pytest.raises(OptionValueError) as excinfo:
        params.size = '1000'
    assert str(excinfo.value) == '"1000" is an invalid value for MultipleChoiceSizeOption'

    params.kind = 'Mega Match'
    with pytest.raises(OptionValueError) as excinfo:
        params.size = '1000'
    assert str(excinfo.value) == '"1000" is an invalid value for MegaMatchSizeOption'

    return


def test_size_options_with_syllabary():

    # The size option applies to multiple choice, match, and mega match quiz types
    # Using Kana table type enables us to cover all the varying size ranges
    params = Parameters()
    params.table = 'Syllabary'

    params.kind = 'Match'
    size_inputs = ['5', '10', '15', '20']
    size_outputs = [MatchSizeOption.FIVE, MatchSizeOption.TEN, MatchSizeOption.FIFTEEN, MatchSizeOption.TWENTY]
    for i, size_in in enumerate(size_inputs):
        params.size = size_in
        assert params.size == size_outputs[i]

    params.kind = 'Multiple Choice'
    size_inputs = ['5', '10', '15', '20']
    size_outputs = [MultipleChoiceSizeOption.FIVE, MultipleChoiceSizeOption.TEN, MultipleChoiceSizeOption.FIFTEEN,
                    MultipleChoiceSizeOption.TWENTY]
    for i, size_in in enumerate(size_inputs):
        params.size = size_in
        assert params.size == size_outputs[i]

    params.kind = 'Mega Match'
    size_inputs = ['4', '6', '8']
    size_outputs = [MegaMatchSizeOption.FOUR, MegaMatchSizeOption.SIX, MegaMatchSizeOption.EIGHT]
    for i, size_in in enumerate(size_inputs):
        params.size = size_in
        assert params.size == size_outputs[i]

    return


def test_prompt_option_order_constraint():

    params = Parameters()
    with pytest.raises(ParameterOrderError) as excinfo:
        params.prompt_type = 'Romaji'
    assert str(excinfo.value) == '"table" parameter must be set before "prompt" parameter'

    return


def test_prompt_option_bad_value():

    params = Parameters()

    params.table = 'Syllabary'
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'invalid'
    assert str(excinfo.value) == f'"invalid" is an invalid value for CharacterOption'

    params.table = 'Vocabulary'
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'invalid'
    assert str(excinfo.value) == f'"invalid" is an invalid value for WordOption'

    return


def test_prompt_option_with_syllabary():

    params = Parameters()
    params.table = 'Syllabary'

    params.prompt_type = 'Romaji'
    assert params.prompt_type == CharacterOption.ROMAJI
    params.prompt_type = 'Hiragana'
    assert params.prompt_type == CharacterOption.HIRAGANA
    params.prompt_type = 'Katakana'
    assert params.prompt_type == CharacterOption.KATAKANA
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'English'
    assert str(excinfo.value) == f'"English" is an invalid value for CharacterOption'
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'Kana'
    assert str(excinfo.value) == f'"Kana" is an invalid value for CharacterOption'
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'Kanji'
    assert str(excinfo.value) == f'"Kanji" is an invalid value for CharacterOption'

    return


def test_prompt_option_with_vocabulary():

    params = Parameters()
    params.table = 'Vocabulary'

    params.prompt_type = 'English'
    assert params.prompt_type == WordOption.ENGLISH
    params.prompt_type = 'Romaji'
    assert params.prompt_type == WordOption.ROMAJI
    params.prompt_type = 'Kana'
    assert params.prompt_type == WordOption.KANA
    params.prompt_type = 'Kanji'
    assert params.prompt_type == WordOption.KANJI
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'Hiragana'
    assert str(excinfo.value) == f'"Hiragana" is an invalid value for WordOption'
    with pytest.raises(OptionValueError) as excinfo:
        params.prompt_type = 'Katakana'
    assert str(excinfo.value) == f'"Katakana" is an invalid value for WordOption'

    return


def test_choice_option_order_constraint():

    # Quiz choice type option depends on both the table and prompt options
    params = Parameters()

    with pytest.raises(ParameterOrderError) as excinfo:
        params.choice_type = 'English'
    assert str(excinfo.value) == '"prompt" parameter must be set before "choice" parameter'

    return


def test_choice_option_bad_value():

    params = Parameters()

    params.table = TableOption.VOCABULARY
    params.prompt_type = WordOption.ROMAJI
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = 'invalid'
    assert str(excinfo.value) == '"invalid" is an invalid value for WordOption'

    params.table = TableOption.SYLLABARY
    params.prompt_type = CharacterOption.ROMAJI
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = 'invalid'
    assert str(excinfo.value) == '"invalid" is an invalid value for CharacterOption'

    return


def test_choice_option_with_vocabulary():

    params = Parameters()
    params.table = TableOption.VOCABULARY

    # ... and with prompt set to "English"
    params.prompt_type = WordOption.ENGLISH
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = WordOption.ENGLISH
    assert str(excinfo.value) == '"English" is an invalid value for choice'
    params.choice_type = WordOption.KANA
    assert params.choice_type == WordOption.KANA
    params.choice_type = WordOption.KANJI
    assert params.choice_type == WordOption.KANJI
    params.prompt_type = WordOption.ROMAJI
    assert params.prompt_type == WordOption.ROMAJI

    # ... and with prompt set to "Kana"
    params.prompt_type = WordOption.KANA
    params.choice_type = WordOption.ENGLISH
    assert params.choice_type == WordOption.ENGLISH
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = WordOption.KANA
    assert str(excinfo.value) == '"Kana" is an invalid value for choice'
    params.choice_type = WordOption.KANJI
    assert params.choice_type == WordOption.KANJI
    params.choice_type = WordOption.ROMAJI
    assert params.choice_type == WordOption.ROMAJI

    # ... and with prompt set to "Kanji"
    params.prompt_type = WordOption.KANJI
    params.choice_type = WordOption.ENGLISH
    assert params.choice_type == WordOption.ENGLISH
    params.choice_type = WordOption.KANA
    assert params.choice_type == WordOption.KANA
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = WordOption.KANJI
    assert str(excinfo.value) == '"Kanji" is an invalid value for choice'
    params.choice_type = WordOption.ROMAJI
    assert params.choice_type == WordOption.ROMAJI

    # ... and with prompt set to "Romaji"
    params.prompt_type = WordOption.ROMAJI
    params.choice_type = WordOption.ENGLISH
    assert params.choice_type == WordOption.ENGLISH
    params.choice_type = WordOption.KANA
    assert params.choice_type == WordOption.KANA
    params.choice_type = WordOption.KANJI
    assert params.choice_type == WordOption.KANJI
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = WordOption.ROMAJI
    assert str(excinfo.value) == '"Romaji" is an invalid value for choice'

    return


def test_choice_option_with_syllabary():

    params = Parameters()
    params.table = TableOption.SYLLABARY

    # ... and with prompt type set to "Hiragana"
    params.prompt_type = CharacterOption.HIRAGANA
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = CharacterOption.HIRAGANA
    assert str(excinfo.value) == '"Hiragana" is an invalid value for choice'
    params.choice_type = CharacterOption.KATAKANA
    assert params.choice_type == CharacterOption.KATAKANA
    params.choice_type = CharacterOption.ROMAJI
    assert params.choice_type == CharacterOption.ROMAJI

    # ... and with prompt type set to "Katakana"
    params.prompt_type = CharacterOption.KATAKANA
    params.choice_type = CharacterOption.HIRAGANA
    assert params.choice_type == CharacterOption.HIRAGANA
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = CharacterOption.KATAKANA
    assert str(excinfo.value) == '"Katakana" is an invalid value for choice'
    params.choice_type = CharacterOption.ROMAJI
    assert params.choice_type == CharacterOption.ROMAJI

    # ... and with prompt type set to "Romaji"
    params.prompt_type = CharacterOption.ROMAJI
    params.choice_type = CharacterOption.HIRAGANA
    assert params.choice_type == CharacterOption.HIRAGANA
    params.choice_type = CharacterOption.KATAKANA
    assert params.choice_type == CharacterOption.KATAKANA
    with pytest.raises(OptionValueError) as excinfo:
        params.choice_type = CharacterOption.ROMAJI
    assert str(excinfo.value) == '"Romaji" is an invalid value for choice'

    return
