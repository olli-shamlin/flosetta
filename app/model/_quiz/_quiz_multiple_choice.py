
from app import FlosettaException
from app.data_paths import QUIZ_ITEMS_FILE
from app.model import Syllabary
from app.model import Vocabulary
from app.model import Word
from app.model import Character
from ._options import TableOption
from ._options import CharacterOption
from ._options import WordOption
from ._parameters import Parameters
from ._quiz_abc import Item
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
    def __init__(self, prompt: Word | Character, choices: list[Word | Character]):
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
        self._results: Optional[list[str]] = None

        num_quiz_items = int(params.size.value)

        # Select the prompt & choice words
        corpus = Vocabulary() if params.table == TableOption.VOCABULARY else Syllabary()
        elements = list(corpus.values())
        prompt_words = sample(elements, num_quiz_items)
        prompt_word_keys = [w.key for w in prompt_words]
        other_words = [w for w in elements if w.key not in prompt_word_keys]
        choice_words = sample(other_words, (num_quiz_items * 4))
        choice_words = _chunk_list(choice_words, 4)

        self._items: list[MultipleChoiceItem] = []
        for i, prompt_word in enumerate(prompt_words):
            choices = [prompt_word] + choice_words[i]
            shuffle(choices)
            item = MultipleChoiceItem(prompt_word, choices)
            self._items.append(item)

        # # TODO This if-then-else block can be reduced.  The conditional just needs to set a "corpus" variable
        # # TODO and the code that randomly selects items from the corpus can be "common" / after the if-then-else
        # TODO OBSOLETE if params.table == TableOption.VOCABULARY:
        # TODO OBSOLETE     vocabulary = Vocabulary()
        # TODO OBSOLETE     words = [w for w in vocabulary.values()]
        # TODO OBSOLETE     prompt_words = sample(words, num_quiz_items)
        # TODO OBSOLETE     prompt_word_ids = [w.key for w in prompt_words]
        # TODO OBSOLETE     other_words = [w for w in words if w.key not in prompt_word_ids]
        # TODO OBSOLETE     alt_choice_words = sample(other_words, (num_quiz_items * 4))
        # TODO OBSOLETE     alt_choice_words = _chunk_list(alt_choice_words, 4)
        # TODO OBSOLETE else:
        # TODO OBSOLETE     assert params.table == TableOption.SYLLABARY
        # TODO OBSOLETE     syllabary = Syllabary()
        # TODO OBSOLETE     characters = [c for c in syllabary.values()]
        # TODO OBSOLETE     prompt_words = sample(characters, num_quiz_items)
        # TODO OBSOLETE     prompt_word_ids = [w.key for w in prompt_words]
        # TODO OBSOLETE     other_words = [w for w in characters if w.key not in prompt_word_ids]
        # TODO OBSOLETE     alt_choice_words = sample(other_words, (num_quiz_items * 4))
        # TODO OBSOLETE     alt_choice_words = _chunk_list(alt_choice_words, 4)
        # TODO OBSOLETE
        # TODO OBSOLETE self._items: list[MultipleChoiceItem] = []
        # TODO OBSOLETE for i, prompt_word in enumerate(prompt_words):
        # TODO OBSOLETE
        # TODO OBSOLETE     if params.prompt_type == WordOption.ENGLISH:
        # TODO OBSOLETE         prompt = prompt_word.english
        # TODO OBSOLETE     elif params.prompt_type == WordOption.KANA:
        # TODO OBSOLETE         prompt = prompt_word.kana
        # TODO OBSOLETE     elif params.prompt_type in [CharacterOption.ROMAJI, WordOption.ROMAJI]:
        # TODO OBSOLETE         prompt = prompt_word.romaji
        # TODO OBSOLETE     elif params.prompt_type == CharacterOption.HIRAGANA:
        # TODO OBSOLETE         prompt = prompt_word.hiragana
        # TODO OBSOLETE     else:  # params.prompt_type == 'Katakana'
        # TODO OBSOLETE         assert params.prompt_type == CharacterOption.KATAKANA
        # TODO OBSOLETE         prompt = prompt_word.katakana
        # TODO OBSOLETE
        # TODO OBSOLETE     if params.choice_type == WordOption.ENGLISH:
        # TODO OBSOLETE         answer = prompt_word.english
        # TODO OBSOLETE         choices = [w.english for w in alt_choice_words[i]] + [answer]
        # TODO OBSOLETE         shuffle(choices)
        # TODO OBSOLETE     elif params.choice_type == WordOption.KANA:
        # TODO OBSOLETE         answer = prompt_word.kana
        # TODO OBSOLETE         choices = [w.kana for w in alt_choice_words[i]] + [answer]
        # TODO OBSOLETE         shuffle(choices)
        # TODO OBSOLETE     elif params.choice_type in [CharacterOption.ROMAJI, WordOption.ROMAJI]:
        # TODO OBSOLETE         answer = prompt_word.romaji
        # TODO OBSOLETE         choices = [w.romaji for w in alt_choice_words[i]] + [answer]
        # TODO OBSOLETE         shuffle(choices)
        # TODO OBSOLETE     elif params.choice_type == CharacterOption.HIRAGANA:
        # TODO OBSOLETE         answer = prompt_word.hiragana
        # TODO OBSOLETE         choices = [w.hiragana for w in alt_choice_words[i]] + [answer]
        # TODO OBSOLETE         shuffle(choices)
        # TODO OBSOLETE     else:  # params.choice_type == 'Katakana'
        # TODO OBSOLETE         assert params.choice_type == CharacterOption.KATAKANA
        # TODO OBSOLETE         answer = prompt_word.katakana
        # TODO OBSOLETE         choices = [w.katakana for w in alt_choice_words[i]] + [answer]
        # TODO OBSOLETE         shuffle(choices)
        # TODO OBSOLETE
        # TODO OBSOLETE     item = MultipleChoiceItem(prompt, answer, choices)
        # TODO OBSOLETE    self._items.append(item)

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

