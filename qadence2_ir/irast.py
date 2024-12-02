"""Definition of the abstract syntax tree (AST) for Qadence 2 IR.

This module defines the abstract syntax tree (AST) in Qadence 2 IR. The AST is used in the front-
end to IR compilation. Implementations of `IRBuilder`, defined in `qadence2-ir.irbuilder`,
translate front-end code to the AST defined here. Then, the tools in `qadence2-ir.factory_tools`
can be used to manipulate an `AST` instance and build valid IR instructions from the AST.
"""

from __future__ import annotations

from enum import Flag, auto
from typing import Any, TypeVar

InputType = TypeVar("InputType")
Arguments = tuple[Any, ...]
Attributes = dict[str, Any]


class AST:
    """Represents an instruction sequence as an abstract syntax tree (AST).

    The initialization of this class must be done using the specific constructors.

    Constructors:

    - AST.numeric(value): For numerical values.
    - AST.input_variable(name, size, trainable): For literal variables.
    - AST.callable(fn_name, *args): For classical functions.
    - AST.support(target, control): For qubit indices.
    - AST.quantum_op(name, support, *args): For quantum operators with and without parameters.
    - AST.sequence(*q_ops): For sequences of quantum operations.
    - AST.add(lhs, rhs): For addition, lhs + rhs.
    - AST.sub(lhs, rhs): For subtraction, lhs - rhs.
    - AST.mul(lhs, rhs): For multiplication, lhs * rhs.
    - AST.div(lhs, rhs): For division, lhs / rhs.
    - AST.rem(lhs, rhs): For remainder, lhs % rhs.
    - AST.pow(base, power): For power, base ** power.
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
        """Base constructor method.

        To void arbitrary initialization, this class must be initialized with one of the standard
        constructors provided. This method hides the initialization from the regular `__new__` to
        enforce that.

        Args:
            tag: A Tag indicating the AST type. Has one of the following values: `QuantumOperator`,
                `Sequence`, `Support`, `Call`, `InputVariable`, `Numeric`.
            head: A string identifier of the AST object.
            args: Optional arguments for specific constructors.
            attrs: Optional attributes for specific constructors.

        Returns:
            ast: A newly constructed AST object.
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

        Returns:
            ast: A numerical value AST.
        """

        return cls.__construct__(cls.Tag.Numeric, "", value)

    @classmethod
    def input_variable(cls, name: str, size: int, trainable: bool, **attributes: Any) -> AST:
        """Create an AST-input variable.

        Args:
            name: The variable's name.
            size: Number of slots to be reserved for the variable, 1 for scalar values and n>1 for
                array variables.
            trainable: A boolean flag to indicate if the variable is intend to be optimized or
                used as a constant during the run.
            attributes: Extra flags, values or dictionaries that can provide more context to the
                backends.

        Returns:
            ast: An input variable AST.
        """

        return cls.__construct__(cls.Tag.InputVariable, name, size, trainable, **attributes)

    @classmethod
    def callable(cls, name: str, *args: AST) -> AST:
        """Create an AST-function object.

        Args:
            name: The function name.
            args: Arguments to be passed to the function.

        Returns:
            ast: A callable AST.
        """

        return cls.__construct__(cls.Tag.Call, name, *args)

    @classmethod
    def support(cls, target: tuple[int, ...], control: tuple[int, ...]) -> AST:
        """Create an AST-support object used to indicate to which qubits a quantum operation is
        applied.

        Args:
            target: A tuple of indices a quantum operator is acting on.
            control: A tuple of indices a quantum operator uses as control qubits.

        Returns:
            ast: A support AST.
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

        Returns:
            ast: A quantum operator AST.
        """

        support = cls.support(target, control)
        return cls.__construct__(cls.Tag.QuantumOperator, name, support, *args, **attributes)

    @classmethod
    def sequence(cls, *quantum_operators: Any) -> AST:
        """Create an AST-sequence of quantum operators objects.

        Args:
            quantum_operators: Sequence of quantum operators to be applied by the backend in the
                given order.

        Returns:
            ast: An AST-sequence of quantum operators.
        """

        return cls.__construct__(cls.Tag.Sequence, "", *quantum_operators)

    # Arithmetic constructors
    @classmethod
    def add(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic addition.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.

        Returns:
            ast: An AST callable adding `lhs` and `rhs`.
        """

        return cls.callable("add", lhs, rhs)

    @classmethod
    def sub(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic subtraction.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.

        Returns:
            ast: An AST callable subtracting `rhs` from `lhs`.
        """

        return cls.callable("sub", lhs, rhs)

    @classmethod
    def mul(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic multiplication.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.

        Returns:
            ast: An AST callable multiplying `lhs` and `rhs`.
        """

        return cls.callable("mul", lhs, rhs)

    @classmethod
    def div(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic division.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.

        Returns:
            ast: An AST callable dividing `lhs` by `rhs`.
        """

        return cls.callable("div", lhs, rhs)

    @classmethod
    def rem(cls, lhs: AST, rhs: AST) -> AST:
        """Create an AST-arithmetic remainder.

        Args:
            lhs: Left-hand side operand.
            rhs: Right-hand side operand.

        Returns:
            ast: An AST callable; remainder or `lhs` and `rhs`.
        """

        return cls.callable("rem", lhs, rhs)

    @classmethod
    def pow(cls, base: AST, power: AST) -> AST:
        """Create an AST-arithmetic power.

        Args:
            base: Base operand.
            power: Power operand.

        Returns:
            ast: An AST callable of `base` to the power `power`.
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
        result = f"{self._tag}('{self._head}', "
        result += ", ".join(map(str, self._args))
        if len(self._attrs) > 0:
            result += ", "
            result += ", ".join([f"{key}={repr(val)}" for key, val in self._attrs.items()])
        return result + ")"
