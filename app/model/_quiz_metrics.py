
class QuizMetrics:

    def __init__(self, quizzed: int = 0, correct: int = 0, consecutive_correct: int = 0, consecutive_wrong: int = 0):
        self._dirty: bool = False
        self._quizzed: int = quizzed
        self._correct: int = correct
        self._consecutive_correct: int = consecutive_correct
        self._consecutive_wrong: int = consecutive_wrong
        return

    @property
    def quizzed(self) -> int:
        return self._quizzed

    @property
    def correct(self) -> int:
        return self._correct

    @property
    def consecutive_correct(self) -> int:
        return self._consecutive_correct

    @property
    def consecutive_incorrect(self) -> int:
        return self._consecutive_wrong

    def increment(self, correct: bool):
        self._quizzed += 1
        if correct:
            self._correct += 1
            self._consecutive_correct += 1
            self._consecutive_wrong = 0
        else:
            self._consecutive_correct = 0
            self._consecutive_wrong += 1
        self._dirty = True

    @property
    def is_non_zero(self) -> bool:
        # return True if any of the metrics are not zero (0).
        return self._quizzed != 0 or self._correct or self._consecutive_correct or self._consecutive_wrong

    @property
    def serialized(self) -> dict[str, int]:
        return {'quizzed': self._quizzed, 'correct': self._correct,
                'consecutive_correct': self._consecutive_correct,
                'consecutive_wrong': self._consecutive_wrong}


def deserialize(d: dict[str, int]) -> QuizMetrics:
    return QuizMetrics(d['quizzed'], d['correct'], d['consecutive_correct'], d['consecutive_wrong'])
