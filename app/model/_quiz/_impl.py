
from ._parameters import Parameters
from ._options import QuizTypeOption
from ._quiz_abc import Quiz
from ._quiz_multiple_choice import MultipleChoiceQuiz


def create_quiz(params: Parameters) -> Quiz:

    quiz_type_map = {
        QuizTypeOption.MULTIPLE_CHOICE: MultipleChoiceQuiz,
        # QuizTypeOption.MATCH: None,
        # QuizTypeOption.MEGA_MATCH: None,
        # QuizTypeOption.KANA_TABLE: None,
    }

    try:
        quiz_cls = quiz_type_map[params.kind]
        quiz_inst = quiz_cls(params)
        quiz_inst.render_javascript()
    except KeyError as e:
        raise NotImplementedError(f'{params.kind} quiz')

    return quiz_inst
