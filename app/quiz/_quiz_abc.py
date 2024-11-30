
from ._options import TableOption
# TODO OBSOLETE CORPORA: from app.model import Entry
from app.corpora import Element
# TODO OBSOLETE from app.model import Word
# TODO OBSOLETE from app.model import Character
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
    # TODO OBSOLETE COPORA: def __init__(self, prompt: Entry, choices: list[Entry]):
    # TODO OBSOLETE COPORA:     self._prompt: Entry = prompt
    # TODO OBSOLETE COPORA:     # TODO OBSOLETE self._answer: Word | Character = answer
    # TODO OBSOLETE COPORA:     self._choices: list[Entry] = choices
    # TODO OBSOLETE COPORA:     self._responses: Optional[list[Entry]] = None
    # TODO OBSOLETE COPORA:     return
    def __init__(self, prompt: Element, choices: list[Element]):
        self._prompt: Element = prompt
        # TODO OBSOLETE self._answer: Word | Character = answer
        self._choices: list[Element] = choices
        self._responses: Optional[list[Element]] = None
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
    # TODO OBSOLETE CORPORA: def prompt(self) -> Entry:
    def prompt(self) -> Element:
        return self._prompt

    # TODO OBSOLETE @property
    # TODO OBSOLETE def answer(self) -> Word | Character:
    # TODO OBSOLETE     return self._answer
    # TODO OBSOLETE
    @property
    # TODO OBSOLETE CORPORA: def choices(self) -> list[Entry]:
    def choices(self) -> list[Element]:
        return self._choices

    @property
    # TODO OBSOLETE CORPORA: def responses(self) -> Optional[list[Entry]]:
    def responses(self) -> Optional[list[Element]]:
        return self._responses

    @responses.setter
    # TODO OBSOLETE CORPORA: def responses(self, responses: list[Entry]) -> None:
    def responses(self, responses: list[Element]) -> None:
        self._responses = responses

    @property
    def transport_format(self) -> str:
        # TODO This is really an abstract method; WordItem and CharacterItem must provide actual implementations
        return ''


class WordItem(Item):

    @property
    def transport_format(self) -> str:
        return '<WORD-TRANSPORT>'


class CharacterItem(Item):

    @property
    def transport_format(self) -> str:
        # This method renders a character quiz item in the transport format the client side
        # code expects when executing a quiz. More specifically, this routine generates
        # JavaScript code that looks like the following:
        #
        #   new CharacterElement(ITEM-KEY, new Map([[ELEMENT-FORM, VALUE], ...]), PROMPT-FORM, CHOICE-FORM)
        #
        # where
        #   - ITEM-KEY: self.key

        return '<CHARACTER-TRANSPORT>'
        #
        # def tab(n) -> str:
        #     return '   ' * n
        # new_line = '\n'
        #
        # prelude = new_line
        # prelude += tab(2) + self.prompt.transport_format + ', ' + new_line
        # prelude += tab(2) + 'new Map([' + new_line
        #
        # transport_choices = ''
        # for i, choice in enumerate(self.choices):
        #     transport_choices += tab(3) + f'["{choice.key}", {choice.transport_format}],' + new_line
        #     # transport_choices += choice.transport_format
        #
        # postlude = tab(2) + '])' + new_line  # close the Map constructor call
        # postlude += tab(1) + ');'            # close the push() method call
        #
        # return prelude + transport_choices + postlude


class Quiz:

    def __init__(self, params: Parameters):
        self._params: Parameters = params
        self._items: Optional[list[Item]] = None

    @property
    def items(self) -> list[Item]:
        return self._items

    @property
    def transport_format(self) -> str:
        # This method currently renders a multiple choice quiz in the transport format the client side
        # code expects when executing a quiz. More specifically, this routine generates JavaScript code
        # that looks like the following:
        #
        #   function quiz_items() {
        #       const quiz_corpus = [];
        #       quiz_corpus.push(ELEMENT-TRANSPORT-FORMAT);
        #       ... REPEATED N-1 TIMES WHERE N IS THE NUMBER OF ITEMS IN THE QUIZ ...
        #       return quiz_corpus;
        #   }

        newline = '\n'

        def tab(n: int = 1) -> str:
            return '   ' * n

        prelude: str = 'function quiz_items() {' + newline
        prelude += tab(1) + 'const quiz = [];' + newline

        items: str = ''
        for i, item in enumerate(self.items):
            i += 1
            next_transport_item = tab(1) + f'const item_{i} = [];' + newline
            for j, choice in enumerate(item.choices):
                j += 1
                next_transport_item += tab(1) + f'item_{i}.push({choice.transport_format}>);' + newline
            items += next_transport_item

        postlude = tab(1) + 'return quiz;'
        postlude += '}'

        return prelude + items + postlude

    def create_transport(self) -> None:

        with open(QUIZ_ITEMS_FILE, 'w') as fh:
            fh.write(self.transport_format)

        flogger.note(f'quiz transport file created: {QUIZ_ITEMS_FILE}')
        return
