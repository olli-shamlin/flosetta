
from enum import auto
from enum import Enum
from enum import unique
from ._exceptions import OptionValueError

# Valid/possible values for quiz options/parameters are coded as enums.
# Option values may be passed in/out in either the enum member value or as a text str.
# The text str form of an option value is derived from its enum member name.
# The QuizParamEnum type must be able to
#   (1) generate the text str form for a value
#   (2) translate an option value from text str form to enum member value
#   (3) translate an option value from enum member value to text str form


class Option(Enum):

    @classmethod
    def option_name(cls, member) -> str:
        return member.name.replace('_', ' ').title()

    @classmethod
    def valid_values(cls) -> list[str]:
        return sorted([cls.option_name(t) for t in cls])

    @classmethod
    # TODO OBSOLETE def to_member(cls, name: str) -> dict[str, int]:
    def to_member(cls, name: str):
        mp = {cls.option_name(t): t for t in cls}
        if name not in mp.keys():
            raise OptionValueError(cls.__name__, name)
        return mp[name]


@unique
class TableOption(Option):
    # The type of data the user can choose to be quizzed on.
    VOCABULARY = auto()
    SYLLABARY = auto()


@unique
class QuizTypeOption(Option):
    # The type of quizzes a user can choose.
    MULTIPLE_CHOICE = auto()
    MATCH = auto()
    KANA_TABLE = auto()
    MEGA_MATCH = auto()
    FILL_IN_THE_BLANK = auto()


@unique
class CharacterOption(Option):
    ROMAJI = auto()
    HIRAGANA = auto()
    KATAKANA = auto()


@unique
class WordOption(Option):
    ENGLISH = auto()
    ROMAJI = auto()
    KANA = auto()
    KANJI = auto()


class SizeOption(Option):

    @classmethod
    def option_name(cls, member) -> str:
        mp = {t: t.value for t in cls}
        return mp[member]


@unique
class MultipleChoiceSizeOption(SizeOption):
    FIVE = '5'
    TEN = '10'
    FIFTEEN = '15'
    TWENTY = '20'


@unique
class MatchSizeOption(SizeOption):
    FIVE = '5'
    TEN = '10'
    FIFTEEN = '15'
    TWENTY = '20'


@unique
class MegaMatchSizeOption(SizeOption):
    # Note for a size n value, the quiz match table will be an n*n square
    FOUR = '4'
    SIX = '6'
    EIGHT = '8'
