
from ._exceptions import OptionNotAllowed
from ._exceptions import OptionValueError
from ._exceptions import ParameterOrderError

from ._options import TableOption
from ._options import QuizTypeOption
from ._options import WordOption
from ._options import CharacterOption
from ._options import MatchSizeOption
from ._options import MegaMatchSizeOption
from ._options import MultipleChoiceSizeOption

from ._parameters import Parameters

from ._quiz_types import Quiz
from ._quiz_types import MultipleChoiceQuiz
from ._quiz_types import MatchQuiz
from ._quiz_types import MegaMatchQuiz
from ._quiz_types import TableQuiz
from ._quiz_types import FillInTheBlankQuiz


def create_quiz(params: Parameters) -> Quiz:

    quiz_type_map: dict = {
        QuizTypeOption.MULTIPLE_CHOICE: MultipleChoiceQuiz,
        QuizTypeOption.MATCH: MatchQuiz,
        QuizTypeOption.MEGA_MATCH: MegaMatchQuiz,
        QuizTypeOption.KANA_TABLE: TableQuiz,
        QuizTypeOption.FILL_IN_THE_BLANK: FillInTheBlankQuiz,
    }

    try:
        quiz_cls = quiz_type_map[params.kind]
        quiz_inst = quiz_cls(params)
        # TODO not ready for prime time: quiz_inst.create_transport()
    except KeyError as e:
        raise NotImplementedError(f'{params.kind} quiz')

    return quiz_inst
