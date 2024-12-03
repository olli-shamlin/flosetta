
from dataclasses import dataclass
from dataclasses import field
from itertools import islice
from random import sample

from config import Config
from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora import Element
from app.corpora import Word
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

    def process_results(self, results_from_client: list[dict]) -> dict:

        results = {
            'num_questions': len(self.questions),
            'num_correct': 0,
            'num_wrong': 0,
            'pct_correct': -1,
            'details': [],
        }

        def echo(e) -> str:
            if isinstance(e, Word):
                r = '; '.join([f'english: {e.english}', f'romaji: {e.romaji}', f'kana: {e.kana}',
                               f'kanji: {e.kanji}' if e.kanji else ''])
            else:
                r = '; '.join([f'romaji: {e.romaji}', f'hiragana: {e.hiragana}', f'katakana: {e.katakana}'])
            return r

        corpus = Corpus(CorpusType.VOCABULARY if self.params.table == TableOption.VOCABULARY else CorpusType.SYLLABARY)
        for i, next_questions_results in enumerate(results_from_client):
            next_question_summary = {
                'correct_answer': next_questions_results['expected'] == next_questions_results['actual'],
                'choices': [echo(e) for e in self.questions[i].elements],
                'answer': echo(corpus[next_questions_results['expected']]),
                'response': echo(corpus[next_questions_results['actual']]),
            }
            results['details'].append(next_question_summary)
            if next_question_summary['correct_answer']:
                # User gave the correct answer to this question
                results['num_correct'] += 1
                corpus[next_questions_results['expected']].increment_metrics(answered_correct=True)
            else:  # User gave the incorrect answer to this question
                results['num_wrong'] += 1
                corpus[next_questions_results['expected']].increment_metrics(answered_correct=False)
                corpus[next_questions_results['actual']].increment_metrics(answered_correct=False)

        results['pct_correct'] = round((results['num_correct'] / results['num_questions']) * 100, 2)

        # Save the updated metrics
        corpus.flush()

        return results


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


def _sample_n_by_5(corpus_id: TableOption, num_questions: TableOption) -> list[Question]:
    elements = _sample_corpus(corpus_id,
                              num_items=(int(num_questions.value) * _NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES))
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
