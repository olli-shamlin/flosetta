
from app import FlosettaException
from app.data_paths import QUIZ_ITEMS_FILE
# TODO OBSOLETE CORPORA: from app.model import Syllabary
# TODO OBSOLETE CORPORA: from app.model import Vocabulary
# TODO OBSOLETE CORPORA: from app.model import Word
# TODO OBSOLETE CORPORA: from app.model import Character
from app.corpora import Corpus
from app.corpora import CorpusType
from ._options import TableOption
from ._options import CharacterOption
from ._options import WordOption
from ._parameters import Parameters
from ._quiz_abc import Item
from ._quiz_abc import CharacterItem
from ._quiz_abc import WordItem
from ._quiz_abc import Quiz
from itertools import islice
from random import sample
from random import shuffle
from typing import Optional


def _chunk_list(arr_range, arr_size):
    arr_range = iter(arr_range)
    answer = iter(lambda: tuple(islice(arr_range, arr_size)), ())
    answer = [list(i) for i in answer]
    return answer


class MultipleChoiceItem(Item):

    # TODO OBSOLETE def __init__(self, prompt: Word | Character, answer: Word | Character, choices: list[Word | Character]):
    # TODO OBSOLETE     # TODO the Item class shouldn't hold the prompt, answer, and choices; the set of corpus items that
    # TODO OBSOLETE     # need to be help is going to vary across types of quizzes
    # TODO OBSOLETE     super().__init__(prompt, answer, choices)
    def __init__(self, prompt: Item, choices: list[Item]):
        # TODO the Item class shouldn't hold the prompt, answer, and choices; the set of corpus items that
        # need to be help is going to vary across types of quizzes
        super().__init__(prompt, choices)
        return

    # TODO OBSOLETE @property
    # TODO OBSOLETE def prompt(self) -> Word | Character:
    # TODO OBSOLETE     return self.prompt
    # TODO OBSOLETE
    # TODO OBSOLETE @property
    # TODO OBSOLETE def answer(self) -> Word | Character:
    # TODO OBSOLETE     return self.answer
    # TODO OBSOLETE
    # TODO OBSOLETE @property
    # TODO OBSOLETE def choices(self) -> list[Word | Character]:
    # TODO OBSOLETE     return self.choices
    # TODO OBSOLETE
    # TODO OBSOLETE @property
    # TODO OBSOLETE def response(self) -> Word | Character:
    # TODO OBSOLETE     assert self.response is not None
    # TODO OBSOLETE     return self.response
    # TODO OBSOLETE
    # TODO OBSOLETE @response.setter
    # TODO OBSOLETE def response(self, r: Word | Character):
    # TODO OBSOLETE     if self.response is None:
    # TODO OBSOLETE         raise FlosettaException(f'response has not been set for {self.answer.key}')
    # TODO OBSOLETE     super()._responses = r
    # TODO OBSOLETE     return
    # TODO OBSOLETE
    @property
    def answered_correct(self) -> bool:
        return self.answer == self.response


class MultipleChoiceQuiz(Quiz):

    def __init__(self, params: Parameters):

        super().__init__(params)
        self._items: list[Item] = []
        self._results: Optional[list[str]] = None

        # Are we building a quiz with words or characters?
        # TODO OBSOLETE CORPORA: corpus = Vocabulary() if params.table == TableOption.VOCABULARY else Syllabary()
        corpus = Corpus(CorpusType.VOCABULARY if params.table == TableOption.VOCABULARY else CorpusType.SYLLABARY)

        # How many questions are we including in this quiz?
        num_questions = int(params.size.value)

        # Randomly select the total number of corpus items (num_questions * 5) that are needed for this quiz
        # TODO OBSOLETE CORPORA: elements = sample(list(corpus.values()), num_questions * 5)
        elements = sample(list(corpus), num_questions * 5)
        shuffle(elements)
        elements = _chunk_list(elements, 5)

        # TODO: This passage of code (for loop below definitely; 3 lines above possibly) are not as readable as they
        # TODO: could/should be.  Variable names are confusing/ambigous, I think.  E.g., "choices" may be better than
        # TODO: "elements" here.
        for e in elements:
            prompt_item = sample(e, 1)[0]
            self._items.append(MultipleChoiceItem(prompt_item, e))

        # for e in elements:
        #     # randomly pick an element from this chunk to be this question's prompt
        #     prompt_element = sample(e, 1)[0]
        #     prompt_item = Item(prompt_element)
        #     self._items.append(MultipleChoiceItem(prompt_item, [Item(f) for f in e]))
        # corpus = Vocabulary() if params.table == TableOption.VOCABULARY else Syllabary()
        # elements = list(corpus.values())
        # prompt_words = sample(elements, num_quiz_items)
        # prompt_word_keys = [w.key for w in prompt_words]
        # other_words = [w for w in elements if w.key not in prompt_word_keys]
        # choice_words = sample(other_words, (num_quiz_items * 4))
        # choice_words = _chunk_list(choice_words, 4)
        #
        # is_word_quiz = params.table == TableOption.VOCABULARY
        # prompt_words = [MultipleChoiceItem(w) for w in prompt_words]
        # choice_words = [MultipleChoiceItem(w) for w in choice_words]
        # for i, prompt_word in enumerate(prompt_words):
        #     choices = [prompt_word] + choice_words[i]
        #     shuffle(choices)
        #     item = WordItem(prompt_word, choices) if is_word_quiz else CharacterItem(prompt_word, choices)
        #     self._items.append(item)

        return

    @property
    def items(self) -> list[MultipleChoiceItem]:
        return self._items

    def add_results(self, results: list[str]) -> None:
        assert self._results is None
        assert len(results) == len(self._items)
        for i, item in enumerate(self._items):
            item.response = results[i]
        return

    @property
    def correct(self) -> int:
        assert all([i.response is not None for i in self._items])
        return len([i for i in self._items if i.answered_correct])

    @property
    def incorrect(self) -> int:
        assert all([i.response is not None for i in self._items])
        return len([i for i in self._items if not i.answered_correct])

    # TODO OBSOLETE ? I think this gets replaced by the create_transport() method
    def render_javascript(self) -> None:

        def tab(n: int):
            return '   ' * n

        prelude: list[str] = [
            'function quiz_items() {',
            tab(1) + 'return [',
        ]

        item_lines: list[str] = []
        quote = '"'
        for item in self._items:
            next_items_lines: list[str] = [
                tab(2) + '{',
                tab(3) + f'prompt: "{item.prompt}",',
                tab(3) + f'answer: "{item.answer}",',
                tab(3) + f'choices: [{", ".join([(quote + c + quote) for c in item.choices])}]',
                tab(2) + '},'
            ]
            item_lines += next_items_lines

        postlude: list[str] = [
            tab(1) + '];',
            '}'
        ]

        lines = [ln + '\n' for ln in (prelude + item_lines + postlude)]

        with open(QUIZ_ITEMS_FILE, 'w') as fh:
            fh.writelines(lines)

        return

