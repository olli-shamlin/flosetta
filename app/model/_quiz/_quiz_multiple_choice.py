
from app.data_paths import QUIZ_ITEMS_FILE
from app.model import Syllabary
from app.model import Vocabulary
from ._options import TableOption
from ._options import CharacterOption
from ._options import WordOption
from ._parameters import Parameters
from ._quiz_abc import Quiz
from itertools import islice
from random import sample
from random import shuffle
from typing import Optional


def _chunk_list(arr_range, arr_size):
    arr_range = iter(arr_range)
    return list(iter(lambda: tuple(islice(arr_range, arr_size)), ()))


class MultipleChoiceItem:

    def __init__(self, prompt: str, answer: str, choices: list[str]):
        self._prompt: str = prompt
        self._answer: str = answer
        self._choices: list[str] = choices
        self._response: Optional[str] = None

    @property
    def prompt(self) -> str:
        return self._prompt

    @property
    def answer(self) -> str:
        return self._answer

    @property
    def choices(self) -> list[str]:
        return self._choices

    @property
    def response(self) -> str:
        assert self._response is not None
        return self._response

    @response.setter
    def response(self, r: str):
        assert self._response is None
        self._response = r
        return

    @property
    def answered_correct(self) -> bool:
        assert self._response is not None
        return self._answer == self._response


class MultipleChoiceQuiz(Quiz):

    def __init__(self, params: Parameters):

        super().__init__(params)
        self._results: Optional[list[str]] = None

        num_quiz_items = int(params.size.value)
        if params.table == TableOption.VOCABULARY:
            vocabulary = Vocabulary()
            words = [w for w in vocabulary.values()]
            prompt_words = sample(words, num_quiz_items)
            prompt_word_ids = [w.key for w in prompt_words]
            other_words = [w for w in words if w.key not in prompt_word_ids]
            alt_choice_words = sample(other_words, (num_quiz_items * 4))
            alt_choice_words = _chunk_list(alt_choice_words, 4)
        else:
            assert params.table == TableOption.SYLLABARY
            syllabary = Syllabary()
            characters = [c for c in syllabary.values()]
            prompt_words = sample(characters, num_quiz_items)
            prompt_word_ids = [w.key for w in prompt_words]
            other_words = [w for w in characters if w.key not in prompt_word_ids]
            alt_choice_words = sample(other_words, (num_quiz_items * 4))
            alt_choice_words = _chunk_list(alt_choice_words, 4)

        self._items: list[MultipleChoiceItem] = []
        for i, prompt_word in enumerate(prompt_words):

            if params.prompt_type == WordOption.ENGLISH:
                prompt = prompt_word.english
            elif params.prompt_type == WordOption.KANA:
                prompt = prompt_word.kana
            elif params.prompt_type in [CharacterOption.ROMAJI, WordOption.ROMAJI]:
                prompt = prompt_word.romaji
            elif params.prompt_type == CharacterOption.HIRAGANA:
                prompt = prompt_word.hiragana
            else:  # params.prompt_type == 'Katakana'
                assert params.prompt_type == CharacterOption.KATAKANA
                prompt = prompt_word.katakana

            if params.choice_type == WordOption.ENGLISH:
                answer = prompt_word.english
                choices = [w.english for w in alt_choice_words[i]] + [answer]
                shuffle(choices)
            elif params.choice_type == WordOption.KANA:
                answer = prompt_word.kana
                choices = [w.kana for w in alt_choice_words[i]] + [answer]
                shuffle(choices)
            elif params.choice_type in [CharacterOption.ROMAJI, WordOption.ROMAJI]:
                answer = prompt_word.romaji
                choices = [w.romaji for w in alt_choice_words[i]] + [answer]
                shuffle(choices)
            elif params.choice_type == CharacterOption.HIRAGANA:
                answer = prompt_word.hiragana
                choices = [w.hiragana for w in alt_choice_words[i]] + [answer]
                shuffle(choices)
            else:  # params.choice_type == 'Katakana'
                assert params.choice_type == CharacterOption.KATAKANA
                answer = prompt_word.katakana
                choices = [w.katakana for w in alt_choice_words[i]] + [answer]
                shuffle(choices)

            item = MultipleChoiceItem(prompt, answer, choices)
            self._items.append(item)

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

