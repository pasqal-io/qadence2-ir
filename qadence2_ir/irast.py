from __future__ import annotations

from enum import Flag, auto
from typing import Any, TypeVar

InputType = TypeVar("InputType")
Arguments = tuple[Any, ...]
Attributes = dict[str, Any]


class AST:
    """A class to keep a clean version of the instruction sequence to be converted
    into a list of Model instructions.

    The initilization of this class must be done using the specific constructors.

    Constructors:
        - AST.numeric(value): For numerical values.
        - AST.input_variable(name, size, trainable): For literal variables.
        - AST.binary_op(op, lhs, rhs): For binary operation where the order of the operation
            matters, like power, division, and subtraction,
        - AST.binary_op_comm(op, lhs, rhs): For binary operation where the operands commute, like
            multiplication and addition.
        - AST.callable(fn_name, *args): For classical functions.
        - AST.support(target, control): For qubit indices.
        - AST.quantum_op(name, support, *args): For quantum operators with and without parameters.
        - AST.sequence(*q_ops): For sequences of quantum operations.
    """

    class Tag(Flag):
        Sequence = auto()
        QuantumOperator = auto()
        Support = auto()
        Call = auto()
        BinaryOperation = auto()
        CommutativeBinaryOperation = auto()
        InputVariable = auto()
        Numeric = auto()

    _tag: Tag
    _head: str
    _args: tuple[Any, ...]
    _attrs: dict[Any, Any]

    @property
    def tag(self) -> Tag:
        return self._tag

    @property
    def head(self) -> str:
        return self._head

    @property
    def args(self) -> tuple[Any, ...]:
        return self._args

    @property
    def attrs(self) -> dict[Any, Any]:
        return self._attrs

    # Constructors
    @classmethod
    def __construct__(cls, tag: Tag, head: str, *args: Any, **attrs: Any) -> AST:
        """To void arbitrary initialisation, the user must use one of the standard constructors
        provided. This method hides the initilisation from the regular `__new__` to enforce that.
        """

        token = super().__new__(cls)
        token._tag = tag
        token._head = head
        token._args = args
        token._attrs = attrs
        return token

    @classmethod
    def numeric(cls, value: complex | float) -> AST:
        """Create an AST-numeric object.

        Arguments:
            - value: Numerical value to be converted in the Qadence-IR AST.
        """

        return cls.__construct__(cls.Tag.Numeric, "", value)

    @classmethod
    def input_variable(cls, name: str, size: int, trainable: bool, **attributes: Any) -> AST:
        """Create an AST-input variable.

        Arguments:
            - name: Variable's name.
            - size: Number of slots to be reserved for the variable, 1 for scalar values and n>1 for
                array variables.
            - trainable: A boolean flag to indicate if the variable is intend to be optimised or
                used as a constand during the run.
            - attributes: Extra flags, values or dictionaries that can provide more context to the
                backends.
        """

        return cls.__construct__(cls.Tag.InputVariable, name, size, trainable, **attributes)

    @classmethod
    def binary_op(cls, op: str, lhs: AST, rhs: AST) -> AST:
        """Create an AST-binary operation.

        This constructor is meant to be used with non-commutative operations.
            lhs op rhs ≠ rhs op lhs

        Arguments:
            - op: Operator.
            - lhs: Left-hand side term
            - rhs: Right-hand side term
        """

        return cls.__construct__(cls.Tag.BinaryOperation, op, lhs, rhs)

    @classmethod
    def binary_op_comm(cls, op: str, lhs: AST, rhs: AST) -> AST:
        """Create an AST-binary operation (commutative).

        This constructor is meant to be used with commutative operations.
            lhs op rhs == rhs op lhs

        Arguments:
            - op: Operator.
            - lhs: Left-hand side term
            - rhs: Right-hand side term
        """

        return cls.__construct__(cls.Tag.CommutativeBinaryOperation, op, lhs, rhs)

    @classmethod
    def callable(cls, name: str, *args: Any) -> AST:
        """Create an AST-function object.

        Arguments:
            - name: Function name.
            - args: Arguments to be passed to the function.
        """

        return cls.__construct__(cls.Tag.Call, name, *args)

    @classmethod
    def support(cls, target: tuple[int, ...], control: tuple[int, ...]) -> AST:
        """Create an AST-support object used to indicate to which qubits a quantum operation is
        applied.

        Arguments:
            - target: A tuple of indices a quantum operator is acting on.
            - control: A tuple of indices a quantum operator uses as control qubits.
        """

        return cls.__construct__(cls.Tag.Support, "", target, control)

    @classmethod
    def quantum_op(
        cls,
        name: str,
        target: tuple[int, ...],
        control: tuple[int, ...],
        *args: Any,
        **attributes: Any,
    ) -> AST:
        """Create an AST-quantum operator.

        Arguments:
            - name: Operator's name.
            - target: A tuple of indices a quantum operator is acting on.
            - control: A tuple of indices a quantum operator uses as control qubits.
            - args: Arguments to be passed to parameteric quantum operators. Non-parametric
                operators like Puali gates are treated as a parametric operator with no arguments.
            - attributes: Extra flags, values or dictionaries that can provide more context to the
                backends.
        """

        support = cls.support(target, control)
        return cls.__construct__(cls.Tag.QuantumOperator, name, support, *args, **attributes)

    @classmethod
    def sequence(cls, *quantum_operators: Any) -> AST:
        """Create an AST-sequence of quantum operators objects.

        Arguments:
            - quantum_operators: Sequence of quantum operators to be applied by the backend it the
                given order.
        """

        return cls.__construct__(cls.Tag.Sequence, "", *quantum_operators)

    # Predicates
    @property
    def is_numeric(self) -> bool:
        return self._tag == AST.Tag.Numeric

    @property
    def is_input_variable(self) -> bool:
        return self._tag == AST.Tag.InputVariable

    @property
    def is_binary_op(self) -> bool:
        return self._tag == AST.Tag.BinaryOperation

    @property
    def is_commutative_binary_op(self) -> bool:
        return self._tag == AST.Tag.CommutativeBinaryOperation

    @property
    def is_callable(self) -> bool:
        return self._tag == AST.Tag.Call

    @property
    def is_support(self) -> bool:
        return self._tag == AST.Tag.Support

    @property
    def is_quantum_op(self) -> bool:
        return self._tag == AST.Tag.QuantumOperator

    @property
    def is_sequence(self) -> bool:
        return self._tag == AST.Tag.Sequence

    def __hash__(self) -> int:
        if self.is_commutative_binary_op:
            return hash((self._tag, self._head, frozenset(self._args)))

        return hash((self._tag, self._head, self._args))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AST):
            return NotImplemented

        if self._tag != other._tag:
            return False

        if self.is_commutative_binary_op:
            return (
                self._head == other._head
                and set(self._args) == set(other._args)
                and self._attrs == other._attrs
            )

        return (
            self._head == other._head and self._args == other._args and self._attrs == other._attrs
        )

    def __repr__(self) -> str:
        return f"{self._tag}({self._head}, {self._args}, {self._attrs})"
