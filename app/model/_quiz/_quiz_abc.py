
from app.model import Word, Character
from app.data_paths import QUIZ_ITEMS_FILE
from app.flogger import flogger
from ._parameters import Parameters
from typing import Optional


class Item:

    # TODO create and ABC for Word & Character; it would be better if quiz classes didn't have to know the
    # TODO differences between the two
    #
    # TODO the set of parameters for this __init__ method definitely favors the multiple choice quiz type
    # TODO Ie, they are specific to that type of quiz; parameters for match quizzes will be different.
    # TODO Point being this is not the right signature for an ABC Item class!!
    # TODO OBSOLETE def __init__(self, prompt: Word | Character, answer: Word | Character, choices: list[Word | Character]):
    # TODO OBSOLETE     self._prompt: Word | Character = prompt
    # TODO OBSOLETE     self._answer: Word | Character = answer
    # TODO OBSOLETE     self._choices: list[Word | Character] = choices
    # TODO OBSOLETE     self._responses: Optional[list[Word | Character]] = None
    def __init__(self, prompt: Word | Character, choices: list[Word | Character]):
        self._prompt: Word | Character = prompt
        # TODO OBSOLETE self._answer: Word | Character = answer
        self._choices: list[Word | Character] = choices
        self._responses: Optional[list[Word | Character]] = None
        return
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

    # TODO OBSOLETE @property
    # TODO OBSOLETE def answer(self) -> Word | Character:
    # TODO OBSOLETE     return self._answer
    # TODO OBSOLETE
    @property
    def choices(self) -> list[Word | Character]:
        return self._choices

    @property
    def responses(self) -> Optional[list[Word | Character]]:
        return self._responses

    @responses.setter
    def responses(self, responses: list[Word | Character]) -> None:
        self._responses = responses

    @property
    def transport_format(self) -> str:
        return f'[TRANSPORT ITEM: {self.prompt.key}]'


class Quiz:

    def __init__(self, params: Parameters):
        self._params: Parameters = params
        self._items: Optional[list[Item]] = None

    @property
    def items(self) -> list[Item]:
        return self._items

    @property
    def transport_format(self) -> str:

        prelude: str = '[PRELUDE] '

        items_transport: str = ''
        for item in self.items:
            items_transport += item.transport_format + ' '

        postlude: str = '[POSTLUDE]'

        return prelude + items_transport + postlude

    def create_transport(self) -> None:

        with open(QUIZ_ITEMS_FILE, 'w') as fh:
            fh.write(self.transport_format)

        flogger.note(f'quiz transport file created: {QUIZ_ITEMS_FILE}')
        return
