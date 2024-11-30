
from dataclasses import dataclass
from itertools import islice
from random import sample

from config import Config
from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora import Element
from app.corpora._store.serializer import json_encoder
from app.quiz import Parameters
from app.quiz import TableOption


_NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES = 5


@dataclass
class Question:
    elements: list[Element]

    @property
    def as_dict(self) -> list[dict]:
        return [e.as_dict for e in self.elements]


@dataclass
class Quiz:
    params: Parameters
    questions: list[Question] = None

    @property
    def as_dict(self) -> dict:
        return {'a_prompt': self.params.prompt_type.name.lower(),
                'b_prompt': self.params.choice_type.name.lower(),
                'questions': [q.as_dict for q in self.questions]}

    @property
    def transport(self) -> str:
        return json_encoder(self.as_dict, indent=None)


@dataclass
class MultipleChoiceQuiz(Quiz):

    def __post_init__(self):
        self.questions = _sample_n_by_5(self.params.table, self.params.size)


@dataclass
class MatchQuiz(Quiz):

    def __post_init__(self):
        self.questions = _sample_n_by_5(self.params.table, self.params.size)


@dataclass
class MegaMatchQuiz(Quiz):

    def __post_init__(self):
        number_of_items = int((self.params.size ** 2) / 2)
        element_sample = _sample_corpus(self.params.table, num_items=number_of_items)
        question = Question(element_sample)
        self.questions = [question]


@dataclass
class TableQuiz(Quiz):

    def __post_init__(self):
        cat_filter = 'Basic' if not Config.TEST_MODE else 'category 1'
        self.questions = [Question([c for c in Corpus(CorpusType.SYLLABARY) if c.category == cat_filter])]


@dataclass
class FillInTheBlankQuiz(Quiz):

    def __post_init__(self):
        corpus_sample = _sample_corpus(self.params.table, num_items=self.params.size)
        self.questions = [Question([e]) for e in corpus_sample]


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
