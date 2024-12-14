
from dataclasses import dataclass
from itertools import islice
from random import sample
from random import shuffle

from app.corpora import Corpus
from app.corpora import CorpusType
from app.corpora import Element
from app.corpora import Word
from app.corpora._store.serializer import json_encoder
from ._parameters import Parameters
# TODO OBSOLETE ISSUE 22 from ._options import SizeOption
# TODO OBSOLETE ISSUE 22 from ._options import TableOption


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
    def name(self) -> str:
        raise NotImplementedError(f'app.quiz._quiz_types.Quiz.name: must be implemented by subclass')

    @property
    def html_template(self) -> str:
        raise NotImplementedError(f'app.quiz._quiz_types.Quiz.html_template: must be implemented by subclass')

    @property
    def as_dict(self) -> dict:
        # TODO OBSOLETE ISSUE 22         return {'a_prompt': self.params.prompt.name.lower(),
        # TODO OBSOLETE ISSUE 22         'b_prompt': self.params.choice.name.lower(),
        # TODO OBSOLETE ISSUE 22         'questions': [q.as_dict for q in self.questions]}
        # TODO OBSOLETE ISSUE 22 return {'a_prompt': self.params.prompt,
        # TODO OBSOLETE ISSUE 22         'b_prompt': self.params.choice,
        # TODO OBSOLETE ISSUE 22         'questions': [q.as_dict for q in self.questions]}
        return {'parameters': self.params.as_dict,
                'questions': [q.as_dict for q in self.questions]}

    @property
    def transport(self) -> str:
        return json_encoder(self.as_dict, indent=None)

    def process_results(self, results_from_client: list[dict]) -> dict:
        raise NotImplementedError(f'app.quiz._quiz_types.Quiz.process_results(): must be implemented by subclass')


@dataclass
class MultipleChoiceQuiz(Quiz):

    def __post_init__(self):
        self.questions = _sample_n_by_5(self.params.table, self.params.size)

    @property
    def name(self) -> str:
        return 'Multiple Choice Quiz'

    @property
    def html_template(self) -> str:
        return 'quiz_multiple_choice.html'

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

        # TODO OBSOLETE ISSUE 22 corpus = Corpus(CorpusType.VOCABULARY if self.params.table == TableOption.VOCABULARY else CorpusType.SYLLABARY)
        corpus = Corpus(CorpusType.VOCABULARY if self.params.table == 'Vocabulary Words' else CorpusType.SYLLABARY)
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
class MatchQuiz(Quiz):

    def __post_init__(self):
        self.questions = _sample_n_by_5(self.params.table, self.params.size)

    @property
    def name(self) -> str:
        return 'Match Quiz'

    @property
    def html_template(self) -> str:
        return 'quiz_match.html'

    def process_results(self, results_from_client: list[dict]) -> dict:
        raise NotImplementedError('app.quiz._quiz_types.MatchQuiz.process_results()')


@dataclass
class MegaMatchQuiz(Quiz):

    def __post_init__(self):
        sample_size = int((self.params.size ** 2) / 2)
        element_sample = _sample_corpus(self.params.table, sample_size)
        shuffle(element_sample)
        self.questions = [Question(element_sample)]

    @property
    def name(self) -> str:
        return 'Mega Match'

    @property
    def html_template(self) -> str:
        return 'quiz_mega_match.html'


@dataclass
class KanaTableQuiz(Quiz):

    def __post_init__(self):
        self.questions = [Question([c for c in Corpus(CorpusType.SYLLABARY) if c.category == 'Basic'])]
        shuffle(self.questions)

    @property
    def name(self) -> str:
        return 'Kana Table'

    @property
    def html_template(self) -> str:
        return 'quiz_kana_table.html'


@dataclass
class FillInTheBlankQuiz(Quiz):

    def __post_init__(self):
        corpus_sample = _sample_corpus(self.params.table, num_items=self.params.size)
        self.questions = [Question([e]) for e in corpus_sample]
        shuffle(self.questions)

    @property
    def name(self) -> str:
        return 'Fill In The Blank'

    @property
    def html_template(self) -> str:
        return 'quiz_fill_in_the_blank.html'


# TODO OBSOLETE ISSUE 22 def _sample_n_by_5(corpus_id: TableOption, num_questions: int) -> list[Question]:
def _sample_n_by_5(corpus_id: str, num_questions: int) -> list[Question]:
    elements = _sample_corpus(corpus_id,
                              num_items=(num_questions * _NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES))
    chunked_elements = _chunk_list(elements, _NUM_MATCH_AND_MULTIPLE_CHOICE_QUESTION_CHOICES)
    questions: list[Question] = []
    for chunk in chunked_elements:
        next_question = Question(chunk)
        questions.append(next_question)
    return questions


# TODO OBSOLETE ISSUE 22 def _sample_corpus(corpus_id: TableOption, num_items: int) -> list[Element]:
# TODO OBSOLETE ISSUE 22     corpus = Corpus(CorpusType.VOCABULARY if corpus_id == TableOption.VOCABULARY else CorpusType.SYLLABARY)
def _sample_corpus(corpus_id: str, num_items: int) -> list[Element]:
    corpus = Corpus(CorpusType.VOCABULARY if corpus_id == 'Vocabulary' else CorpusType.SYLLABARY)
    elements = sample(corpus, num_items)
    return elements


def _chunk_list(arr_range, arr_size):
    arr_range = iter(arr_range)
    answer = iter(lambda: tuple(islice(arr_range, arr_size)), ())
    answer = [list(i) for i in answer]
    return answer
