# TODO:
# - [ ] docstrings

from __future__ import annotations

from enum import Flag, auto
from typing import Any, TypeVar

from .types import Support

InputType = TypeVar("InputType")
Arguments = tuple[Any, ...]
Attributes = dict[str, Any]


class AST:

    class Tag(Flag):
        Sequence = auto()
        QuantumOperator = auto()
        Call = auto()
        BinaryOperation = auto()
        InputVariable = auto()
        Numeric = auto()

    tag: Tag
    head: str
    args: tuple[Any, ...]
    attrs: dict[Any, Any]

    def __hash__(self) -> int:
        return hash((self.tag, self.head, self.args))

    # Constructors
    @classmethod
    def __construct__(cls, tag: Tag, head: str, *args: Any, **attrs: Any) -> AST:
        token = cls()
        token.tag = tag
        token.head = head
        token.args = args
        token.attrs = attrs
        return token

    @classmethod
    def numeric(cls, value: complex | float) -> AST:
        return cls.__construct__(cls.Tag.Numeric, "", value)

    @classmethod
    def input_variable(cls, name: str, **attributes: Any) -> AST:
        return cls.__construct__(cls.Tag.InputVariable, name, **attributes)

    @classmethod
    def binary_op(cls, op: str, lhs: AST, rhs: AST) -> AST:
        return cls.__construct__(cls.Tag.BinaryOperation, op, lhs, rhs)

    @classmethod
    def callable(cls, name: str, *args: Any) -> AST:
        return cls.__construct__(cls.Tag.Call, name, *args)

    @classmethod
    def quantum_op(
        cls,
        name: str,
        target: tuple[int, ...],
        control: tuple[int, ...],
        *args: Any,
        **attributes: Any,
    ) -> AST:
        support = Support(target=target, control=control)
        return cls.__construct__(cls.Tag.QuantumOperator, name, support, *args, **attributes)

    @classmethod
    def sequence(cls, *args: Any) -> AST:
        return cls.__construct__(cls.Tag.Sequence, "", *args)

    # Prdeicates
    @property
    def is_numeric(self) -> bool:
        return self == AST.Tag.Numeric

    @property
    def is_input_variable(self) -> bool:
        return self == AST.Tag.InputVariable

    @property
    def is_binary_op(self) -> bool:
        return self == AST.Tag.BinaryOperation

    @property
    def is_callable(self) -> bool:
        return self == AST.Tag.Call

    @property
    def is_quantum_op(self) -> bool:
        return self == AST.Tag.QuantumOperator

    @property
    def is_sequence(self) -> bool:
        return self == AST.Tag.Sequence
