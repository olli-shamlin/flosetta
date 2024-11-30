
from abc import ABC
from dataclasses import dataclass
from itertools import islice
from random import sample

from config import Config
from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora import Element
from app.quiz import Parameters
from app.quiz import TableOption


_NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES = 5


@dataclass
class Question:
    elements: list[Element]

    @property
    def transport_format(self):
        raise NotImplementedError('app.quiz._quiz_types.Question.transport_format')
    #
    # @property
    # def number_of_elements(self) -> int:
    #     return len(self.elements)


@dataclass
class Quiz(ABC):
    params: Parameters
    questions: list[Question] = None

    @property
    def transport_format(self):
        raise NotImplementedError('app.quiz._quiz_types.Question.transport_format')

    # @property
    # def number_of_questions(self) -> int:
    #     return self.params.size
    #
    # TODO: Don't think we need a_format & b_format properties on the Quiz class. Only need these values when
    # TODO: generating the transport and can derive them from params at that time.
    # @property
    # def a_format(self):
    #     raise NotImplementedError('app.quiz._quiz_types.Question.a_format')
    #
    # @property
    # def b_format(self):
    #     raise NotImplementedError('app.quiz._quiz_types.Question.b_format')
    #
    # @property
    # @abstractmethod
    # def total_number_of_elements(self) -> int:
    #     pass
    #
    # @total_number_of_elements.setter
    # def total_number_of_elements(self, n: int) -> None:
    #     raise NotImplementedError('app.quiz._quiz_types.Quiz.total_number_of_elements setter')
    #
    # @total_number_of_elements.deleter
    # def total_number_of_elements(self) -> None:
    #     raise NotImplementedError('app.quiz._quiz_types.Quiz.total_number_of_elements deleter')


@dataclass
class MultipleChoiceQuiz(Quiz):

    def __post_init__(self):
        self.questions = _sample_n_by_5(self.params.table, self.params.size)
    #
    # @property
    # def total_number_of_elements(self) -> int:
    #     return self.params.size * _NUM_MULTIPLE_CHOICE_QUESTION_CHOICES


@dataclass
class MatchQuiz(Quiz):

    def __post_init__(self):
        self.questions = _sample_n_by_5(self.params.table, self.params.size)
    #
    # @property
    # def total_number_of_elements(self) -> int:
    #     return self.params.size * _NUM_MATCH_QUESTION_CHOICES


@dataclass
class MegaMatchQuiz(Quiz):

    def __post_init__(self):
        number_of_items = int((self.params.size ** 2) / 2)
        element_sample = _sample_corpus(self.params.table, num_items=number_of_items)
        question = Question(element_sample)
        self.questions = [question]
    #
    # @property
    # def total_number_of_elements(self) -> int:
    #     return (self.params.size ** 2) / 2


@dataclass
class TableQuiz(Quiz):

    def __post_init__(self):
        cat_filter = 'Basic' if not Config.TEST_MODE else 'category 1'
        self.questions = [Question([c for c in Corpus(CorpusType.SYLLABARY) if c.category == cat_filter])]
    #
    # @property
    # def total_number_of_elements(self) -> int:
    #     # TODO: May not need to derive this property value by instantiating a Corpus in this method.
    #     # TODO: As long as this getter is called after an instance has been created, this property's
    #     # TODO: value can be calculated using the elements field of the questions field (I think)
    #     syllabary = Corpus(CorpusType.SYLLABARY)
    #     return len([c for c in syllabary if c.category == 'Basic'])


@dataclass
class FillInTheBlankQuiz(Quiz):

    def __post_init__(self):
        corpus_sample = _sample_corpus(self.params.table, num_items=self.params.size)
        self.questions = [Question([e]) for e in corpus_sample]
    #
    # @property
    # def total_number_of_elements(self) -> int:
    #     return self.params.size


def _sample_n_by_5(corpus_id: TableOption, num_questions: int) -> list[Question]:
    elements = _sample_corpus(corpus_id, num_items=(num_questions * _NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES))
    chunked_elements = _chunk_list(elements, _NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES)
    questions: list[Question] = []
    for chunk in chunked_elements:
        next_question = Question(chunk)
        questions.append(next_question)
    return questions


def _sample_corpus(corpus_id: TableOption, num_items: int) -> list[Element]:
    corpus = Corpus(CorpusType.VOCABULARY if corpus_id == TableOption.VOCABULARY else CorpusType.SYLLABARY)
    elements = sample(corpus, num_items)
    return elements


def _chunk_list(arr_range, arr_size):
    arr_range = iter(arr_range)
    answer = iter(lambda: tuple(islice(arr_range, arr_size)), ())
    answer = [list(i) for i in answer]
    return answer
