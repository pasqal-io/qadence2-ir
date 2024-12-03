"""Definition of all types supported in the IR.

This module is the defacto definition of the IR. A unit of IR code can only consist of instances of
the classes defined in this module. An IR `Model` defines a complete set of instructions for a
backend to execute as a task. The instructions a `Model` can take can be divided into two groups;
classical and quantum related instructions:

- Classical:
    - `Alloc`: Allocates memory for holding variable values.
    - `Assign`: Assigns a value to a variable.
    - `Load`: Retrieves a value from a variable.
    - `Call`: Executes a classical function.
- Quantum:
    - `AllocQubits`: Allocates qubits for the computation.
    - `QuInstruct`: Executes a quantum instruction.
    - `Support`: Defines on which qubit(s) and with what role, target or control, a `QuInstruct`
        should act.
"""

from __future__ import annotations

from typing import Any, Literal


class Alloc:
    """Memory allocation for a parameter that is either a scalar value or an array of values.

    With this class an allocation of memory is made for a parameter that is a scalar value, if
    `size = 1` or an array of values of length `n` if `size = n`. The type for the allocation is
    defined by the backend, therefore it is not defined in the IR.

    Args:
        size: Number of values stored in the parameter, if `size = 1` the parameter is a scalar
            value if `size > 1` the parameter is an array of values.
        trainable: Indicates whether the parameter can be changed during a training loop.
        attributes: Extra flags and information to be used as instructions/suggestions by the
            backend.
    """

    def __init__(self, size: int, trainable: bool, **attributes: Any) -> None:
        self.size = size
        self.is_trainable = trainable
        self.attrs = attributes

    def __repr__(self) -> str:
        params = f"{self.size}, trainable={self.is_trainable}"
        if self.attrs:
            params += f", attrs={self.attrs}"
        return f"{self.__class__.__name__}({params})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Alloc):
            return NotImplemented

        lhs = (self.size, self.is_trainable, self.attrs)
        rhs = (value.size, value.is_trainable, value.attrs)
        return lhs == rhs


class Assign:
    """Assignment of a value to a variable.

    Args:
        variable_name: The name of the variable to assign a value to.
        value: The value to be assigned to the variable.
    """

    def __init__(self, variable_name: str, value: Any) -> None:
        self.variable = variable_name
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.variable)}, {self.value})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Assign):
            return NotImplemented

        lhs = (self.variable, self.value)
        rhs = (value.variable, value.value)
        return lhs == rhs


class Load:
    """Instruction to load the value of a variable.

    Args:
        variable_name: The name of the variable to load.
    """

    def __init__(self, variable_name: str) -> None:
        self.variable = variable_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.variable)})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Load):
            return NotImplemented

        return self.variable == value.variable


class Call:
    """Instruction to call a classical function.

    Args:
        identifier: The identifier of the function to call, i.e. its name.
        args: The arguments that the function should be called with.
    """

    def __init__(self, identifier: str, *args: Any) -> None:
        self.identifier = identifier
        self.args = args

    def __repr__(self) -> str:
        if not self.args:
            return f"{self.__class__.__name__}({repr(self.identifier)})"
        else:
            args = ", ".join(map(repr, self.args))
            return f"{self.__class__.__name__}({repr(self.identifier)}, {args})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Call):
            return NotImplemented

        lhs = (self.identifier, self.args)
        rhs = (value.identifier, value.args)
        return lhs == rhs


class Support:
    """Instruction that specifies the target and optionally control of a `QuInstruct`.

    Generic representation of qubit support, specifying a target and control for a quantum
    instruction. For single qubit operations, a multiple index support indicates apply the
    operation for each index in the support. Both target and control lists must be ordered!

    Args:
        target: Index or indices of qubits to which the operation is applied.
        control: Index or indices of qubits which to which the operation is conditioned to.
    """

    def __init__(
        self,
        target: tuple[int, ...],
        control: tuple[int, ...] | None = None,
    ) -> None:
        self.target = target
        self.control = control or ()

    @classmethod
    def target_all(cls) -> Support:
        return Support(target=())

    def __repr__(self) -> str:
        if not self.target:
            return f"{self.__class__.__name__}.target_all()"

        subspace = f"{self.target}"
        if self.control:
            subspace += f", control={self.control}"

        return f"{self.__class__.__name__}({subspace})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Support):
            return NotImplemented

        lhs = (self.target, self.control)
        rhs = (value.target, value.control)
        return lhs == rhs


class QuInstruct:
    """Instruction to apply a quantum operation to one or more qubit(s).

    Args:
        name: The instruction name compatible with the standard instruction set.
        support: The index of qubits to which the instruction is applied to.
        args: Arguments of the instruction such as angle, duration, amplitude etc.
        attributes: Extra flags and information to be used as instructions/suggestions by the
            backend.
    """

    def __init__(self, name: str, support: Support, *args: Any, **attributes: Any):
        self.name = name
        self.support = support
        self.args = args
        self.attrs = attributes

    def __repr__(self) -> str:
        params = f"{repr(self.name)}, {self.support}"
        args = ", ".join(map(repr, self.args))
        if args:
            params += ", " + args
        if self.attrs:
            params += f", attributes={self.attrs}"
        return f"{self.__class__.__name__}({params})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, QuInstruct):
            return NotImplemented

        lhs = (self.name, self.support, self.args, self.attrs)
        rhs = (value.name, value.support, value.args, value.attrs)
        return lhs == rhs


class AllocQubits:
    """Allocation of qubit in a register of a neutral-atom QPU.

    Args:
        num_qubits: Number of qubits, i.e atoms, to be allocated.
        qubit_positions: A list of discrete coordinates for 2D grid, where (0,0) is the position at
            center of the grid. An empty list will indicate the backend is free to define the
            topology for devices that implement logical qubits.
        grid_type: Allows to select the coordinates sets for 2D grids as "square" (orthogonal) or
            "triangular" (skew). A "linear" will allow the backend to define the shape of the
            register. When the `grid_type` is `None` the backend uses its default structure
            (particular useful when shuttling is available). Default value is `None`.
        grid_scale: Adjust the distance between atoms based on a standard distance defined by the
            backend. Default value is 1.0.
        connectivity: A dictionary that contains the interaction strength between connected qubit
            pairs. It is used with compiler backends that implement crossing-lattice strategies or
            gridless models, such as `pyqtorch`. If the connectivity graph is available, these
            backends may ignore the `qubit_positions`, `grid_type`, and `grid_scale` options.
        options: Extra register related properties that may not be supported by all backends.
    """

    def __init__(
        self,
        num_qubits: int,
        qubit_positions: list[tuple[int, int]] | list[int] | None = None,
        grid_type: Literal["linear", "square", "triangular"] | None = None,
        grid_scale: float = 1.0,
        connectivity: dict[tuple[int, int], float] | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        self.num_qubits = num_qubits
        self.qubit_positions = qubit_positions or []
        self.grid_type = grid_type
        self.grid_scale = grid_scale
        self.connectivity = connectivity or dict()
        self.options = options or dict()

    def __repr__(self) -> str:
        arguments = f"{self.num_qubits}"
        if len(self.qubit_positions) > 0:
            arguments += f", qubit_positions={self.qubit_positions}"
        if self.grid_type is not None:
            arguments += f", grid_type='{self.grid_type}'"
        if self.grid_scale != 1.0:
            arguments += f", grid_scale={self.grid_scale}"
        if len(self.connectivity) > 0:
            arguments += f", connectivity={self.connectivity}"
        if len(self.options) > 0:
            arguments += f", options={self.options}"
        return f"{self.__class__.__name__}({arguments})"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, AllocQubits):
            return NotImplemented

        lhs = (self.num_qubits, self.qubit_positions, self.grid_type, self.grid_scale, self.options)
        rhs = (
            value.num_qubits,
            value.qubit_positions,
            value.grid_type,
            value.grid_scale,
            value.options,
        )
        return lhs == rhs


class Model:
    """Aggregates the minimal information to construct sequence of instructions to execute on a QPU.

    This class defines a unit of IR code. The structure of the class is mainly focused in neutral
    atoms devices but its agnostic nature may make it suitable for any quantum device.

    Args:
        register: Describes the atomic arrangement of the neutral atom register.
        instructions: A list of abstract instructions with their arguments that a backend can use
            to execute a sequence.
        directives: A dictionary containing QPU related options. For instance, it can be used to
            set the Rydberg level to be used or whether to allow digital-analog operations in the
            sequence.
        settings: Backend specific configurations where the user can define for instance, the data
            type like `int64`.
    """

    def __init__(
        self,
        register: AllocQubits,
        inputs: dict[str, Alloc],
        instructions: list[QuInstruct | Assign],
        directives: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
    ) -> None:
        self.register = register
        self.directives = directives or dict()
        self.settings = settings or dict()
        self.inputs = inputs
        self.instructions = instructions

    def __repr__(self) -> str:
        indent = "  "
        result = f"{self.__class__.__name__}(\n"
        result += f"{indent}{self.register},\n"
        result += f"{indent}{'{'}\n"
        for key, value in self.inputs.items():
            result += f"{indent}{indent}'{key}': {value},\n"
        result += f"{indent}{'}'},\n"
        result += f"{indent}[\n"
        for item in self.instructions:
            result += f"{indent}{indent}{item},\n"
        result += f"{indent}]"

        if self.directives != dict():
            result += f",\n{indent}directives={'{'}\n"
            for key, value in self.directives.items():
                result += f"{indent}{indent}'{key}': {value},\n"
            result += f"{indent}{'}'}"
        if self.settings != dict():
            result += f",\n{indent}settings={'{'}\n"
            for key, value in self.settings.items():
                result += f"{indent}{indent}'{key}': {value},\n"
            result += f"{indent}{'}'}"
        result += "\n)"
        return result

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Model):
            return NotImplemented

        lhs = (self.register, self.inputs, self.instructions, self.directives, self.settings)
        rhs = (value.register, value.inputs, value.instructions, value.directives, value.settings)
        return lhs == rhs
