
from app.model import Word, Character
from ._parameters import Parameters
from typing import Optional


class Item:

    # TODO create and ABC for Word & Character; it would be better if quiz classes didn't have to know the
    # TODO differences between the two
    #
    # TODO the set of parameters for this __init__ method definitely favors the multiple choice quiz type
    # TODO Ie, they are specific to that type of quiz; parameters for match quizzes will be different.
    # TODO Point being this is not the right signature for an ABC Item class!!
    def __init__(self, prompt: Word | Character, answer: Word | Character, choices: list[Word | Character]):
        self._prompt: Word | Character = prompt
        self._answer: Word | Character = answer
        self._choices: list[Word | Character] = choices
        self._responses: Optional[list[Word | Character]] = None
        #
        # For Multiple Choice:
        #
        # For Match:
        #
        # For Mega Match:
        #
        # For Kana Table:
        #

    @property
    def prompt(self) -> Word | Character:
        return self._prompt

    @property
    def answer(self) -> Word | Character:
        return self._answer

    @property
    def choices(self) -> list[Word | Character]:
        return self._choices

    @property
    def responses(self) -> list[Word | Character]:
        return self._responses

    @responses.setter
    def responses(self, responses: list[Word | Character]) -> None:
        self._responses = responses


class Quiz:

    def __init__(self, params: Parameters):
        self._params: Parameters = params
        self._items: Optional[list[Item]] = None

    @property
    def items(self) -> list[Item]:
        return self._items
