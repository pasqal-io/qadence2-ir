from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from .irast import AST, Attributes, InputType
from .types import AllocQubits


class AbstractIRBuilder(ABC, Generic[InputType]):
    """A base class to help create new input forms for Qadence2-IR.

    Implementing this class allows the function `ir_compiler_factory` to generate
    the `compile_to_model` function for a new custom input format.
    """

    @staticmethod
    @abstractmethod
    def set_register(input_obj: InputType) -> AllocQubits:
        """Used by the factory to define the qubits register from the input."""

    @staticmethod
    @abstractmethod
    def set_directives(input_obj: InputType) -> Attributes:
        """Use by the factory to set the QPU directives from the input."""

    @staticmethod
    @abstractmethod
    def settings(input_obj: InputType) -> Attributes:
        """Used by the factory to define general settings for simulation and data purposes."""

    @staticmethod
    @abstractmethod
    def parse_sequence(input_obj: InputType) -> AST:
        """Used by the factory to parse a sequence operations acting on the qubit
        register (e.g., quantum circuits, pulse sequences, etc).
        """
