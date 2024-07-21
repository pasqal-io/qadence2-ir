# TODO:
# - [ ] docstrings

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from .irast import InputType, Attributes, AST
from .types import AllocQubits


class AbstractIRBuilder(ABC, Generic[InputType]):

    @staticmethod
    @abstractmethod
    def set_register(input_obj: InputType) -> AllocQubits:
        pass

    @staticmethod
    @abstractmethod
    def set_directives(input_obj: InputType) -> Attributes:
        pass

    @staticmethod
    @abstractmethod
    def settings(input_obj: InputType) -> Attributes:
        pass

    @staticmethod
    @abstractmethod
    def parse_sequence(input_obj: InputType) -> AST:
        pass
