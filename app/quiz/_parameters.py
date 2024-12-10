
from ._options import TableOption
from ._options import QuizTypeOption
from ._options import WordOption
from ._options import CharacterOption

from dataclasses import dataclass


@dataclass
class Parameters:
    kind: QuizTypeOption
    table: TableOption
    prompt: CharacterOption | WordOption
    choice: CharacterOption | WordOption
    size: int

    def __post_init__(self):

        table_map: dict = {
            TableOption.SYLLABARY: CharacterOption,
            TableOption.VOCABULARY: WordOption
        }

        self.kind = QuizTypeOption.to_member(self.kind)
        self.table = TableOption.to_member(self.table)
        self.prompt = table_map[self.table].to_member(self.prompt)
        self.choice = table_map[self.table].to_member(self.choice)

        return
