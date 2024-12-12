
# TODO OBSOLETE ISSUE 22 from ._options import TableOption
# TODO OBSOLETE ISSUE 22 from ._options import QuizTypeOption
# TODO OBSOLETE ISSUE 22 from ._options import WordOption
# TODO OBSOLETE ISSUE 22 from ._options import CharacterOption

from dataclasses import dataclass


@dataclass
class Parameters:
    kind: str
    table: str
    prompt: str
    choice: str
    size: int

    def __post_init__(self):

        valid_kind_values = ['Multiple Choice', 'Match', 'Mega Match', 'Kana Table', 'Fill In The Blank']
        valid_table_values = ['Vocabulary', 'Syllabary']
        valid_format_values = ['English', 'Kana', 'Romaji', 'Hiragana', 'Katakana']
        valid_size_values = [1, 4, 5, 6, 8, 10, 15, 20]

        if self.kind not in valid_kind_values:
            raise ValueError(f'Parameters.__post_init__: "{self.kind}" not a valid value for "kind"')
        if self.table not in valid_table_values:
            raise ValueError(f'Parameters.__post_init__: "{self.table}" not a valid value for "table"')
        if self.prompt not in valid_format_values:
            raise ValueError(f'Parameters.__post_init__: "{self.prompt}" not a valid value for "prompt"')
        if self.choice not in valid_format_values:
            raise ValueError(f'Parameters.__post_init__: "{self.choice}" not a valid value for "choice"')
        if self.size not in valid_size_values:
            raise ValueError(f'Parameters.__post_init__: "{self.size}" not a valid value for "size"')

        # TODO OBSOLETE ISSUE 22         table_map: dict = {
        # TODO OBSOLETE ISSUE 22             TableOption.SYLLABARY: CharacterOption,
        # TODO OBSOLETE ISSUE 22             TableOption.VOCABULARY: WordOption
        # TODO OBSOLETE ISSUE 22         }
        # TODO OBSOLETE ISSUE 22
        # TODO OBSOLETE ISSUE 22 self.kind = QuizTypeOption.to_member(self.kind)
        # TODO OBSOLETE ISSUE 22 self.table = TableOption.to_member(self.table)
        # TODO OBSOLETE ISSUE 22 self.prompt = table_map[self.table].to_member(self.prompt)
        # TODO OBSOLETE ISSUE 22 self.choice = table_map[self.table].to_member(self.choice)
        # TODO OBSOLETE ISSUE 22
        # TODO OBSOLETE ISSUE 22 return
