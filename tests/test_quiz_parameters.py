#
# from app.quiz import Parameters
# from app.quiz import TableOption
# from app.quiz import QuizTypeOption
# from app.quiz import CharacterOption
# from app.quiz import WordOption
# from app.quiz import MatchSizeOption
# from app.quiz import MegaMatchSizeOption
# from app.quiz import MultipleChoiceSizeOption
# from app.quiz import OptionValueError
# from app.quiz import ParameterOrderError
# import pytest
#
#
# class TestParameters:
#
#     def test_table_option_bad_value(self) -> None:
#
#         params = Parameters()
#         with pytest.raises(OptionValueError) as excinfo:
#             params.table = 'invalid'
#         assert str(excinfo.value) == '"invalid" is an invalid value for TableOption'
#
#         return
#
#     def test_table_option(self) -> None:
#
#         params = Parameters()
#
#         params.table = 'Syllabary'
#         assert params.table == TableOption.SYLLABARY
#
#         params.table = 'Vocabulary'
#         assert params.table == TableOption.VOCABULARY
#
#         return
#
#     def test_kind_option_order_constraint(self) -> None:
#
#         params = Parameters()
#
#         with pytest.raises(ParameterOrderError) as excinfo:
#             params.kind = 'Multiple Choice'
#         assert str(excinfo.value) == '"table" parameter must be set before "kind" parameter'
#
#         return
#
#     def test_kind_option_bad_value(self) -> None:
#
#         params = Parameters()
#
#         params.table = 'Syllabary'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.table = 'invalid'
#         assert str(excinfo.value) == '"invalid" is an invalid value for TableOption'
#
#         params.table = 'Vocabulary'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.table = 'invalid'
#         assert str(excinfo.value) == '"invalid" is an invalid value for TableOption'
#
#         return
#
#     def test_kind_option_with_syllabary(self) -> None:
#
#         params = Parameters()
#         params.table = 'Syllabary'
#
#         params.kind = 'Multiple Choice'
#         assert params.kind == QuizTypeOption.MULTIPLE_CHOICE
#         params.kind = 'Match'
#         assert params.kind == QuizTypeOption.MATCH
#         params.kind = 'Kana Table'
#         assert params.kind == QuizTypeOption.KANA_TABLE
#         params.kind = 'Mega Match'
#         assert params.kind == QuizTypeOption.MEGA_MATCH
#
#         return
#
#     def test_kind_option_with_vocabulary(self) -> None:
#
#         params = Parameters()
#         params.table = 'Vocabulary'
#
#         # Only "multiple choice" and "match" quiz types are supported with the Vocabulary table
#         params.kind = 'Multiple Choice'
#         assert params.kind == QuizTypeOption.MULTIPLE_CHOICE
#         params.kind = 'Match'
#         assert params.kind == QuizTypeOption.MATCH
#         with pytest.raises(OptionValueError) as excinfo:
#             params.kind = 'Kana Table'
#         assert str(excinfo.value) == '"Kana Table" is an invalid value for kind'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.kind = 'Mega Match'
#         assert str(excinfo.value) == '"Mega Match" is an invalid value for kind'
#
#         return
#
#     def test_size_option_order_constraint(self) -> None:
#
#         params = Parameters()
#
#         with pytest.raises(ParameterOrderError) as excinfo:
#             params.size = 5
#         assert str(excinfo.value) == '"kind" parameter must be set before "size" parameter'
#
#         return
#
#     def test_size_option_bad_value_with_vocabulary(self) -> None:
#
#         params = Parameters()
#         params.table = 'Vocabulary'
#
#         params.kind = 'Match'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.size = '1000'
#         assert str(excinfo.value) == '"1000" is an invalid value for MatchSizeOption'
#
#         params.kind = 'Multiple Choice'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.size = '1000'
#         assert str(excinfo.value) == '"1000" is an invalid value for MultipleChoiceSizeOption'
#
#         return
#
#     def test_size_option_bad_value_with_syllabary(self) -> None:
#
#         params = Parameters()
#         params.table = 'Syllabary'
#
#         params.kind = 'Match'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.size = '1000'
#         assert str(excinfo.value) == '"1000" is an invalid value for MatchSizeOption'
#
#         params.kind = 'Multiple Choice'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.size = '1000'
#         assert str(excinfo.value) == '"1000" is an invalid value for MultipleChoiceSizeOption'
#
#         params.kind = 'Mega Match'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.size = '1000'
#         assert str(excinfo.value) == '"1000" is an invalid value for MegaMatchSizeOption'
#
#         return
#
#     def test_size_options_with_syllabary(self) -> None:
#
#         # The size option applies to multiple choice, match, and mega match quiz types
#         # Using Kana table type enables us to cover all the varying size ranges
#         params = Parameters()
#         params.table = 'Syllabary'
#
#         params.kind = 'Match'
#         size_inputs = ['5', '10', '15', '20']
#         size_outputs = [MatchSizeOption.FIVE, MatchSizeOption.TEN, MatchSizeOption.FIFTEEN, MatchSizeOption.TWENTY]
#         for i, size_in in enumerate(size_inputs):
#             params.size = size_in
#             assert params.size == size_outputs[i]
#
#         params.kind = 'Multiple Choice'
#         size_inputs = ['5', '10', '15', '20']
#         size_outputs = [MultipleChoiceSizeOption.FIVE, MultipleChoiceSizeOption.TEN, MultipleChoiceSizeOption.FIFTEEN,
#                         MultipleChoiceSizeOption.TWENTY]
#         for i, size_in in enumerate(size_inputs):
#             params.size = size_in
#             assert params.size == size_outputs[i]
#
#         params.kind = 'Mega Match'
#         size_inputs = ['4', '6', '8']
#         size_outputs = [MegaMatchSizeOption.FOUR, MegaMatchSizeOption.SIX, MegaMatchSizeOption.EIGHT]
#         for i, size_in in enumerate(size_inputs):
#             params.size = size_in
#             assert params.size == size_outputs[i]
#
#         return
#
#     def test_prompt_option_order_constraint(self) -> None:
#
#         params = Parameters()
#         with pytest.raises(ParameterOrderError) as excinfo:
#             params.prompt = 'Romaji'
#         assert str(excinfo.value) == '"table" parameter must be set before "prompt" parameter'
#
#         return
#
#     def test_prompt_option_bad_value(self) -> None:
#
#         params = Parameters()
#
#         params.table = 'Syllabary'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'invalid'
#         assert str(excinfo.value) == f'"invalid" is an invalid value for CharacterOption'
#
#         params.table = 'Vocabulary'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'invalid'
#         assert str(excinfo.value) == f'"invalid" is an invalid value for WordOption'
#
#         return
#
#     def test_prompt_option_with_syllabary(self) -> None:
#
#         params = Parameters()
#         params.table = 'Syllabary'
#
#         params.prompt = 'Romaji'
#         assert params.prompt == CharacterOption.ROMAJI
#         params.prompt = 'Hiragana'
#         assert params.prompt == CharacterOption.HIRAGANA
#         params.prompt = 'Katakana'
#         assert params.prompt == CharacterOption.KATAKANA
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'English'
#         assert str(excinfo.value) == f'"English" is an invalid value for CharacterOption'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'Kana'
#         assert str(excinfo.value) == f'"Kana" is an invalid value for CharacterOption'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'Kanji'
#         assert str(excinfo.value) == f'"Kanji" is an invalid value for CharacterOption'
#
#         return
#
#     def test_prompt_option_with_vocabulary(self) -> None:
#
#         params = Parameters()
#         params.table = 'Vocabulary'
#
#         params.prompt = 'English'
#         assert params.prompt == WordOption.ENGLISH
#         params.prompt = 'Romaji'
#         assert params.prompt == WordOption.ROMAJI
#         params.prompt = 'Kana'
#         assert params.prompt == WordOption.KANA
#         params.prompt = 'Kanji'
#         assert params.prompt == WordOption.KANJI
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'Hiragana'
#         assert str(excinfo.value) == f'"Hiragana" is an invalid value for WordOption'
#         with pytest.raises(OptionValueError) as excinfo:
#             params.prompt = 'Katakana'
#         assert str(excinfo.value) == f'"Katakana" is an invalid value for WordOption'
#
#         return
#
#     def test_choice_option_order_constraint(self) -> None:
#
#         # Quiz choice type option depends on both the table and prompt options
#         params = Parameters()
#
#         with pytest.raises(ParameterOrderError) as excinfo:
#             params.choice = 'English'
#         assert str(excinfo.value) == '"prompt" parameter must be set before "choice" parameter'
#
#         return
#
#     def test_choice_option_bad_value(self) -> None:
#
#         params = Parameters()
#
#         params.table = TableOption.VOCABULARY
#         params.prompt = WordOption.ROMAJI
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = 'invalid'
#         assert str(excinfo.value) == '"invalid" is an invalid value for WordOption'
#
#         params.table = TableOption.SYLLABARY
#         params.prompt = CharacterOption.ROMAJI
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = 'invalid'
#         assert str(excinfo.value) == '"invalid" is an invalid value for CharacterOption'
#
#         return
#
#     def test_choice_option_with_vocabulary(self) -> None:
#
#         params = Parameters()
#         params.table = TableOption.VOCABULARY
#
#         # ... and with prompt set to "English"
#         params.prompt = WordOption.ENGLISH
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = WordOption.ENGLISH
#         assert str(excinfo.value) == '"English" is an invalid value for choice'
#         params.choice = WordOption.KANA
#         assert params.choice == WordOption.KANA
#         params.choice = WordOption.KANJI
#         assert params.choice == WordOption.KANJI
#         params.prompt = WordOption.ROMAJI
#         assert params.prompt == WordOption.ROMAJI
#
#         # ... and with prompt set to "Kana"
#         params.prompt = WordOption.KANA
#         params.choice = WordOption.ENGLISH
#         assert params.choice == WordOption.ENGLISH
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = WordOption.KANA
#         assert str(excinfo.value) == '"Kana" is an invalid value for choice'
#         params.choice = WordOption.KANJI
#         assert params.choice == WordOption.KANJI
#         params.choice = WordOption.ROMAJI
#         assert params.choice == WordOption.ROMAJI
#
#         # ... and with prompt set to "Kanji"
#         params.prompt = WordOption.KANJI
#         params.choice = WordOption.ENGLISH
#         assert params.choice == WordOption.ENGLISH
#         params.choice = WordOption.KANA
#         assert params.choice == WordOption.KANA
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = WordOption.KANJI
#         assert str(excinfo.value) == '"Kanji" is an invalid value for choice'
#         params.choice = WordOption.ROMAJI
#         assert params.choice == WordOption.ROMAJI
#
#         # ... and with prompt set to "Romaji"
#         params.prompt = WordOption.ROMAJI
#         params.choice = WordOption.ENGLISH
#         assert params.choice == WordOption.ENGLISH
#         params.choice = WordOption.KANA
#         assert params.choice == WordOption.KANA
#         params.choice = WordOption.KANJI
#         assert params.choice == WordOption.KANJI
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = WordOption.ROMAJI
#         assert str(excinfo.value) == '"Romaji" is an invalid value for choice'
#
#         return
#
#     def test_choice_option_with_syllabary(self) -> None:
#
#         params = Parameters()
#         params.table = TableOption.SYLLABARY
#
#         # ... and with prompt type set to "Hiragana"
#         params.prompt = CharacterOption.HIRAGANA
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = CharacterOption.HIRAGANA
#         assert str(excinfo.value) == '"Hiragana" is an invalid value for choice'
#         params.choice = CharacterOption.KATAKANA
#         assert params.choice == CharacterOption.KATAKANA
#         params.choice = CharacterOption.ROMAJI
#         assert params.choice == CharacterOption.ROMAJI
#
#         # ... and with prompt type set to "Katakana"
#         params.prompt = CharacterOption.KATAKANA
#         params.choice = CharacterOption.HIRAGANA
#         assert params.choice == CharacterOption.HIRAGANA
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = CharacterOption.KATAKANA
#         assert str(excinfo.value) == '"Katakana" is an invalid value for choice'
#         params.choice = CharacterOption.ROMAJI
#         assert params.choice == CharacterOption.ROMAJI
#
#         # ... and with prompt type set to "Romaji"
#         params.prompt = CharacterOption.ROMAJI
#         params.choice = CharacterOption.HIRAGANA
#         assert params.choice == CharacterOption.HIRAGANA
#         params.choice = CharacterOption.KATAKANA
#         assert params.choice == CharacterOption.KATAKANA
#         with pytest.raises(OptionValueError) as excinfo:
#             params.choice = CharacterOption.ROMAJI
#         assert str(excinfo.value) == '"Romaji" is an invalid value for choice'
#
#         return
