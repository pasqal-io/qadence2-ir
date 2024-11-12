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
        AST.numeric(value): For numerical values.
        AST.input_variable(name, size, trainable): For literal variables.
        AST.callable(fn_name, *args): For classical functions.
        AST.support(target, control): For qubit indices.
        AST.quantum_op(name, support, *args): For quantum operators with and without parameters.
        AST.sequence(*q_ops): For sequences of quantum operations.
        AST.add(lhs, rhs): For addition, lhs + rhs.
        AST.sub(lhs, rhs): For subtraction, lhs - rhs.
        AST.mul(lhs, rhs): For multiplication, lhs * rhs.
        AST.div(lhs, rhs): For division, lhs / rhs.
        AST.rem(lhs, rhs): For remainder, lhs % rhs.
        AST.pow(base, power): For power, base ** power.
    """

    class Tag(Flag):
        Sequence = auto()
        QuantumOperator = auto()
        Support = auto()
        Call = auto()
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

        Args:
            value: Numerical value to be converted in the Qadence-IR AST.
        """

        return cls.__construct__(cls.Tag.Numeric, "", value)

    @classmethod
    def input_variable(cls, name: str, size: int, trainable: bool, **attributes: Any) -> AST:
        """Create an AST-input variable.

        Args:
            name: Variable's name.
            size: Number of slots to be reserved for the variable, 1 for scalar values and n>1 for
                array variables.
            trainable: A boolean flag to indicate if the variable is intend to be optimised or
                used as a constand during the run.
            attributes: Extra flags, values or dictionaries that can provide more context to the
                backends.
        """

        return cls.__construct__(cls.Tag.InputVariable, name, size, trainable, **attributes)

    @classmethod
    def callable(cls, name: str, *args: Any) -> AST:
        """Create an AST-function object.

        Args:
            name: Function name.
            args: Arguments to be passed to the function.
        """

        return cls.__construct__(cls.Tag.Call, name, *args)

    @classmethod
    def support(cls, target: tuple[int, ...], control: tuple[int, ...]) -> AST:
        """Create an AST-support object used to indicate to which qubits a quantum operation is
        applied.

        Args:
            target: A tuple of indices a quantum operator is acting on.
            control: A tuple of indices a quantum operator uses as control qubits.
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

        Args:
            name: Operator's name.
            target: A tuple of indices a quantum operator is acting on.
            control: A tuple of indices a quantum operator uses as control qubits.
            args: Arguments to be passed to parameteric quantum operators. Non-parametric
                operators like Puali gates are treated as a parametric operator with no arguments.
            attributes: Extra flags, values or dictionaries that can provide more context to the
                backends.
        """

        support = cls.support(target, control)
        return cls.__construct__(cls.Tag.QuantumOperator, name, support, *args, **attributes)

    @classmethod
    def sequence(cls, *quantum_operators: Any) -> AST:
        """Create an AST-sequence of quantum operators objects.

        Args:
            quantum_operators: Sequence of quantum operators to be applied by the backend in the
                given order.
        """

        return cls.__construct__(cls.Tag.Sequence, "", *quantum_operators)

    # Arithmetic constructors
    @classmethod
    def add(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic addition.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.
        """

        return cls.callable("add", lhs, rhs)

    @classmethod
    def sub(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic subtraction.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.
        """

        return cls.callable("sub", lhs, rhs)

    @classmethod
    def mul(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic multiplication.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.
        """

        return cls.callable("mul", lhs, rhs)

    @classmethod
    def div(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic division.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.
        """

        return cls.callable("div", lhs, rhs)

    @classmethod
    def rem(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic remainder.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.
        """

        return cls.callable("rem", lhs, rhs)

    @classmethod
    def pow(cls, base: AST, power: AST) -> AST:
        """Create an AST-arithmetic power.

        Args:
            base: Base operand.
            power: Power operand.
        """

        return cls.callable("pow", base, power)

    # Predicates
    @property
    def is_numeric(self) -> bool:
        return self._tag == AST.Tag.Numeric

    @property
    def is_input_variable(self) -> bool:
        return self._tag == AST.Tag.InputVariable

    @property
    def is_callable(self) -> bool:
        return self._tag == AST.Tag.Call

    @property
    def is_addition(self) -> bool:
        return self._tag == AST.Tag.Call and self._head == "add"

    @property
    def is_subtraction(self) -> bool:
        return self._tag == AST.Tag.Call and self._head == "sub"

    @property
    def is_multiplication(self) -> bool:
        return self._tag == AST.Tag.Call and self._head == "mul"

    @property
    def is_division(self) -> bool:
        return self._tag == AST.Tag.Call and self._head == "div"

    @property
    def is_remainder(self) -> bool:
        return self._tag == AST.Tag.Call and self._head == "rem"

    @property
    def is_power(self) -> bool:
        return self._tag == AST.Tag.Call and self._head == "pow"

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
        if self.is_addition or self.is_multiplication:
            return hash((self._tag, self._head, frozenset(self._args)))

        return hash((self._tag, self._head, self._args))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AST):
            return NotImplemented

        if self._tag != other._tag or self._head != other._head:
            return False

        if self.is_addition or self.is_multiplication:
            return set(self._args) == set(other._args) and self._attrs == other._attrs

        return self._args == other._args and self._attrs == other._attrs

    def __repr__(self) -> str:
       # args
        result += ", ".join(map(str, self._args))
        # attributes
        result += ", ".join([f"{key}={repr(val)}" for key, val in self._attrs.items()])
        return result + ")"
