
from typing import Optional
from ._options import TableOption
from ._options import QuizTypeOption
from ._options import WordOption
from ._options import CharacterOption
from ._options import MatchSizeOption
from ._options import MegaMatchSizeOption
from ._options import MultipleChoiceSizeOption
from ._options import SizeOption
from ._exceptions import OptionValueError
from ._exceptions import ParameterOrderError
from ._exceptions import OptionNotAllowed

from dataclasses import dataclass


@dataclass
class Parameters:
    kind: QuizTypeOption
    table: TableOption
    prompt: CharacterOption | WordOption
    choice: CharacterOption | WordOption
    size: int

    def __post_init__(self):

        kind_map: dict = {
            QuizTypeOption.MULTIPLE_CHOICE: MultipleChoiceSizeOption,
            QuizTypeOption.MATCH: MatchSizeOption,
            QuizTypeOption.MEGA_MATCH: MegaMatchSizeOption,
            QuizTypeOption.KANA_TABLE: None,
            QuizTypeOption.FILL_IN_THE_BLANK: MultipleChoiceSizeOption,
        }
        table_map: dict = {
            TableOption.SYLLABARY: CharacterOption,
            TableOption.VOCABULARY: WordOption
        }

        self.kind = QuizTypeOption.to_member(self.kind)
        self.table = TableOption.to_member(self.table)
        self.prompt = table_map[self.table].to_member(self.prompt)
        self.choice = table_map[self.table].to_member(self.choice)
        # self.size = self.size.to_member(str(self.size))

        return

# class Parameters:
#     # Encapsulates the options the user is given when setting up a quiz.
#     # Both the set of options and their values vary depending on the type of data being quizzed
#     # on (i.e., vocabulary words or kana characters) and the type of quiz the user chose.
#
#     def __init__(self):
#         self._table: Optional[TableOption] = None
#         self._type: Optional[QuizTypeOption] = None
#         self._size: Optional[int] = None
#         self._prompt: Optional[WordOption | CharacterOption] = None
#         self._choice: Optional[WordOption | CharacterOption] = None
#         self._word_part_of_speech_filter: Optional[list[str]] = None
#         self._word_tag_filter: Optional[list[str]] = None
#         self._kana_category_filter: Optional[list[str]] = None
#
#         return
#
#     @property
#     def table(self) -> TableOption:
#         return self._table
#
#     @table.setter
#     def table(self, value: TableOption | str) -> None:
#         if isinstance(value, str):
#             try:
#                 value = TableOption.to_member(value)
#             except KeyError as e:
#                 raise OptionValueError('table', value)
#         self._table = value
#
#     @property
#     def kind(self) -> QuizTypeOption:
#         return self._type
#
#     @kind.setter
#     def kind(self, value: QuizTypeOption | str) -> None:
#         if self._table is None:
#             raise ParameterOrderError('table', 'kind')
#         value_str = value
#         if isinstance(value, str):
#             value = QuizTypeOption.to_member(value)
#         if self._table == TableOption.VOCABULARY:
#             if value not in [QuizTypeOption.MULTIPLE_CHOICE, QuizTypeOption.MATCH]:
#                 raise OptionValueError('kind', value_str)
#         else:
#             if value not in [t for t in QuizTypeOption]:
#                 raise OptionValueError('kind', value_str)
#         self._type = value
#
#     @property
#     def size(self) -> SizeOption:
#         return self._size
#
#     @size.setter
#     def size(self, value: str) -> None:
#         if self._type is None:
#             raise ParameterOrderError('kind', 'size')
#         if self._type == QuizTypeOption.KANA_TABLE:
#             raise OptionNotAllowed('size')
#
#         if isinstance(value, str):
#             if self._type == QuizTypeOption.MATCH:
#                 value = MatchSizeOption.to_member(value)
#             elif self._type == QuizTypeOption.MULTIPLE_CHOICE:
#                 value = MultipleChoiceSizeOption.to_member(value)
#             elif self._type == QuizTypeOption.MEGA_MATCH:
#                 value = MegaMatchSizeOption.to_member(value)
#             else:
#                 raise OptionNotAllowed('size')
#
#         self._size = value
#
#     @property
#     def prompt_type(self) -> WordOption | CharacterOption:
#         return self._prompt
#
#     @prompt_type.setter
#     def prompt_type(self, value: str | WordOption | CharacterOption) -> None:
#         if self._table is None:
#             raise ParameterOrderError('table', 'prompt')
#         if isinstance(value, str):
#             value = WordOption.to_member(value) if self._table == TableOption.VOCABULARY \
#                 else CharacterOption.to_member(value)
#         self._prompt = value
#
#     @property
#     def prompt_options(self) -> list[str]:
#         return WordOption.valid_values() if self._table == TableOption.VOCABULARY else CharacterOption.valid_values()
#
#     @property
#     def choice_type(self) -> WordOption | CharacterOption:
#         return self._choice
#
#     @choice_type.setter
#     def choice_type(self, value: str | WordOption | CharacterOption) -> None:
#         if self._prompt is None:
#             raise ParameterOrderError('prompt', 'choice')
#         # Valid choice option values are the set of WordOption/CharacterOption values *except* the prompt option value.
#         valid_values = {t: t.name for t in (WordOption if self._table == TableOption.VOCABULARY else CharacterOption)
#                         if t != self._prompt}
#         if isinstance(value, str):
#             value = WordOption.to_member(value) if self._table == TableOption.VOCABULARY \
#                 else CharacterOption.to_member(value)
#         value_as_str = WordOption.option_name(value) if self._table == TableOption.VOCABULARY \
#             else CharacterOption.option_name(value)
#         # Option value cannot be the same as the prompt option value
#         if (value == self._prompt) \
#                 or (value not in valid_values.keys()):
#             raise OptionValueError('choice', value_as_str)
#         self._choice = value
#
#     @property
#     def choice_options(self) -> list[str]:
#         answer: list[str] = self.prompt_options
#         prompt_choice: str = WordOption.option_name(self.prompt_type) if self.table == TableOption.VOCABULARY \
#             else CharacterOption.option_name(self.prompt_type)
#         answer.remove(prompt_choice)
#         return answer
#
#     @property
#     def part_of_speech_filter(self) -> Optional[list[str]]:
#         # return self._word_part_of_speech_filter
#         raise NotImplementedError('quiz.py/Parameters.part_of_speech_filter')
#
#     @part_of_speech_filter.setter
#     def part_of_speech_filter(self, value: list[str]) -> None:
#         # self._word_part_of_speech_filter = value
#         raise NotImplementedError('quiz.py/Parameters.part_of_speech_filter')
#
#     @property
#     def tag_filter(self) -> Optional[list[str]]:
#         # return self._word_tag_filter
#         raise NotImplementedError('quiz.py/Parameters.tag_filter')
#
#     @tag_filter.setter
#     def tag_filter(self, value: list[str]) -> None:
#         # self._word_tag_filter = value
#         raise NotImplementedError('quiz.py/Parameters.tag_filter')
#
#     @property
#     def kana_category_filter(self) -> Optional[list[str]]:
#         # return self._kana_category_filter
#         raise NotImplementedError('quiz.py/Parameters.kana_category_filter')
#
#     @kana_category_filter.setter
#     def kana_category_filter(self, value: list[str]) -> None:
#         # self._kana_category_filter = value
#         raise NotImplementedError('quiz.py/Parameters.kana_category_filter')
