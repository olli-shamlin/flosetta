
from typing import Optional


class QuizMetrics:

    def __init__(self, quizzed: int = 0, correct: int = 0, consecutive_correct: int = 0, consecutive_wrong: int = 0):
        self._dirty: bool = False
        self._quizzed: int = quizzed
        self._correct: int = correct
        self._consecutive_correct: int = consecutive_correct
        self._consecutive_wrong: int = consecutive_wrong
        return

    @property
    def quizzed(self) -> int:
        return self._quizzed

    @property
    def correct(self) -> int:
        return self._correct

    @property
    def consecutive_correct(self) -> int:
        return self._consecutive_correct

    @property
    def consecutive_incorrect(self) -> int:
        return self._consecutive_wrong

    @property
    def is_dirty(self) -> bool:
        return self._dirty

    def increment(self, correct: bool):
        self._quizzed += 1
        if correct:
            self._correct += 1
            self._consecutive_correct += 1
            self._consecutive_wrong = 0
        else:
            self._consecutive_correct = 0
            self._consecutive_wrong += 1
        self._dirty = True

    def synced(self):
        self._dirty = False


class QuizParameters:

    def __init__(self):
        self._table: Optional[str] = None
        self._kind: Optional[str] = None
        self._number_of_items: Optional[int] = None
        self._prompt_type: Optional[str] = None
        self._choice_type: Optional[str] = None
        self._pos_filter: Optional[list[str]] = None
        self._tag_fiter: Optional[list[str]] = None
        self._category_filter: Optional[list[str]] = None
        return

    @property
    def table(self) -> str:
        assert self._table is not None
        return self._table

    @table.setter
    def table(self, table: str):
        table = table.title()
        assert table in ['Vocabulary', 'Kana']
        self._table = table
        return

    @property
    def type_of_quiz(self) -> str:
        assert self._kind is not None
        return self._kind

    @type_of_quiz.setter
    def type_of_quiz(self, kind: str):
        kind = kind.title()
        all_kinds_of_quizzes = ['Multiple Choice', 'Match', 'Fill In The Blank', 'Jigsaw', 'Match Game']
        vocab_kinds_of_quizzes = ['Multiple Choice', 'Match']
        assert (self._table == 'Vocabulary' and kind in vocab_kinds_of_quizzes) or \
               (self._table == 'Kana' and kind in all_kinds_of_quizzes)
        self._kind = kind
        return

    @property
    def number_of_items(self) -> int:
        return self._number_of_items

    @number_of_items.setter
    def number_of_items(self, cnt: int):
        assert cnt in [5, 10, 15, 20]
        self._number_of_items = cnt
        return

    @property
    def prompt_type(self):
        return self._prompt_type

    @prompt_type.setter
    def prompt_type(self, ptype: str):
        assert (self._table == 'Vocabulary' and ptype in ['English', 'Kana', 'Kanji']) or \
               (self._table == 'Kana' and ptype in ['Romaji', 'Hiragana', 'Kanji'])
        assert (self._prompt_type != self._choice_type) or (self._prompt_type is None and self._choice_type is None)
        self._prompt_type = ptype
        return

    @property
    def choice_type(self):
        return self._choice_type

    @choice_type.setter
    def choice_type(self, ctype: str):
        assert (self._table == 'Vocabulary' and ctype in ['English', 'Kana', 'Kanji']) or \
               (self._table == 'Kana' and ctype in ['Romaji', 'Hiragana', 'Kanji'])
        assert self._prompt_type != self._choice_type
        self._choice_type = ctype
        return

    @property
    def part_of_speech_filter(self) -> list[str]:
        # return self._pos_filter
        raise NotImplementedError('quiz.py/QuizParameters.part_of_speech_filter')

    @part_of_speech_filter.setter
    def part_of_speech_filter(self, pos: list[str]):
        # self._pos_filter = pos
        # return
        raise NotImplementedError('quiz.py/QuizParameters.part_of_speech_filter')

    @property
    def tag_filter(self) -> list[str]:
        # return self._tag_fiter
        raise NotImplementedError('quiz.py/QuizParameters.tag_filter')

    @tag_filter.setter
    def tag_filter(self, tags: list[str]):
        # self._tag_fiter = tags
        # return
        raise NotImplementedError('quiz.py/QuizParameters.tag_filter')

    @property
    def category_filter(self) -> list[str]:
        # return self._category_filter
        raise NotImplementedError('quiz.py/QuizParameters.category_filter')

    @category_filter.setter
    def category_filter(self, categories: list[str]):
        # self._category_filter = categories
        # return
        raise NotImplementedError('quiz.py/QuizParameters.category_filter')
