
from ._exceptions import OptionNotAllowed
from ._exceptions import OptionValueError
from ._exceptions import ParameterOrderError

# TODO OBSOLETE ISSUE 22 from ._options import Option
# TODO OBSOLETE ISSUE 22 from ._options import TableOption
# TODO OBSOLETE ISSUE 22 from ._options import QuizTypeOption
# TODO OBSOLETE ISSUE 22 from ._options import WordOption
# TODO OBSOLETE ISSUE 22 from ._options import CharacterOption
# TODO OBSOLETE ISSUE 22 from ._options import MatchSizeOption
# TODO OBSOLETE ISSUE 22 from ._options import MegaMatchSizeOption
# TODO OBSOLETE ISSUE 22 from ._options import MultipleChoiceSizeOption

from ._parameters import Parameters

from ._quiz_types import Quiz
from ._quiz_types import MultipleChoiceQuiz
from ._quiz_types import MatchQuiz
from ._quiz_types import MegaMatchQuiz
from ._quiz_types import TableQuiz
from ._quiz_types import FillInTheBlankQuiz


def create_quiz(params: Parameters) -> Quiz:

    quiz_type_map: dict = {
        # TODO OBSOLETE ISSUE 22 QuizTypeOption.MULTIPLE_CHOICE: MultipleChoiceQuiz,
        # TODO OBSOLETE ISSUE 22 QuizTypeOption.MATCH: MatchQuiz,
        # TODO OBSOLETE ISSUE 22 QuizTypeOption.MEGA_MATCH: MegaMatchQuiz,
        # TODO OBSOLETE ISSUE 22 QuizTypeOption.KANA_TABLE: TableQuiz,
        # TODO OBSOLETE ISSUE 22 QuizTypeOption.FILL_IN_THE_BLANK: FillInTheBlankQuiz,
        'Multiple Choice': MultipleChoiceQuiz,
        'Match': MatchQuiz,
        'Mega Match': MegaMatchQuiz,
        'Kana Table': TableQuiz,
        'Fill In The Blank': FillInTheBlankQuiz,
    }

    try:
        quiz_cls = quiz_type_map[params.kind]
        quiz_inst = quiz_cls(params)
    except KeyError as e:
        raise NotImplementedError(f'{params.kind} quiz')

    return quiz_inst
