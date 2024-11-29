"""Defines an ABC for implementing IR builders.

This module defines the interface to be used by Qadence 2 IR front-ends to compile to IR. A front-
end must implement an `IRBuilder` for the front-end specific input type, so that
`ir_compiler_factory`, defined in `qadence2-ir.factory` can generate a compiler function specific
to the front-end.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic

from .irast import AST, Attributes, InputType
from .types import AllocQubits


class IRBuilder(ABC, Generic[InputType]):
    """Defines the interface of Qadence 2 IR builders for building IR code from front-end input.

    An `IRBuilder` implementation can be used by the `ir_compiler_factory` function, defined in
    `qadence2-ir.factory` to build a compiler function that generates IR code from a specific
    input type as created by a Qadence 2 front-end.
    When subclassing this class, specify the `InputType` that is expected for the implementation,
    i.e. the object type that the specific front-end generates.
    This class is responsible for extracting information about the register, directives, other
    settings and the AST from front-end generated input.
    """

    @staticmethod
    @abstractmethod
    def set_register(input_obj: InputType) -> AllocQubits:
        """Returns a register definition based on an input object.

        Args:
            input_obj: Input for the compilation to IR native to a specific front-end.

        Returns:
            A register definition that is extracted or inferred from `input_obj`.
        """

    @staticmethod
    @abstractmethod
    def set_directives(input_obj: InputType) -> Attributes:
        """Returns directives based on an input object.

        Args:
            input_obj: Input for the compilation to IR native to a specific front-end.

        Returns:
            A specification of all directives that could be extracted from `input_obj`.
        """

    @staticmethod
    @abstractmethod
    def settings(input_obj: InputType) -> Attributes:
        """Returns settings based on an input object.

        Args:
            input_obj: Input for the compilation to IR native to a specific front-end.

        Returns:
            A specification of all settings that could be extracted from `input_obj`.
        """

    @staticmethod
    @abstractmethod
    def parse_sequence(input_obj: InputType) -> AST:
        """Returns an AST definition that represents the operations in input object.

        Args:
            input_obj: Input for the compilation to IR native to a specific front-end.

        Returns:
            An AST definition that represents the operations defined in `input_obj`.
        """
