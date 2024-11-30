
from app import FlosettaException


class OptionValueError(FlosettaException):
    def __init__(self, param_name: str, param_value: str | int):
        self.message = f'"{param_value}" is an invalid value for {param_name}'
        super().__init__(self.message)


class ParameterOrderError(FlosettaException):
    def __init__(self, param1: str, param2: str | int):
        self.message = f'"{param1}" parameter must be set before "{param2}" parameter'
        super().__init__(self.message)


class OptionNotAllowed(FlosettaException):
    def __init__(self, param_name: str):
        self.message = f'"{param_name}" cannot be set for this type of quiz'
        super().__init__(self.message)
