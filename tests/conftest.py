# use this file for configuring test fixtures and
# functions common to every test
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any

import pytest

from qadence2_ir.factory import IRBuilder
from qadence2_ir.irast import AST, Attributes
from qadence2_ir.types import Alloc, AllocQubits, Assign, Model, QuInstruct, Support


@pytest.fixture
def classical_ast() -> AST:
    x = AST.input_variable("x", 1, False)
    three = AST.numeric(3)
    div = AST.div(x, three)
    fn = AST.callable("fn", div, x)

    return fn


@pytest.fixture
def quantum_ast() -> AST:
    x = AST.input_variable("x", 1, False)
    three = AST.numeric(3)
    div = AST.div(x, three)
    fn = AST.callable("fn", div, x)
    q_op = AST.quantum_op("rx", (0,), (1,), fn)

    return q_op


@pytest.fixture
def support_control_target() -> Support:
    return Support((0,), (1,))


@pytest.fixture
def simple_model() -> Model:
    register = AllocQubits(3)
    inputs = {"input1": Alloc(1, False), "input2": Alloc(4, True)}
    instructions: list[Assign | QuInstruct] = [
        Assign("var1", 10),
        QuInstruct("CNOT", Support((0,), (1,))),
        QuInstruct("RX", Support.target_all(), 3.14),
    ]
    return Model(register, inputs, instructions)


@pytest.fixture
def model_with_directives_settings(simple_model: Model) -> Model:
    new_model = deepcopy(simple_model)
    new_model.directives = {"option1": 3, "option2": True}
    new_model.settings = {"setting1": 18.0}
    return new_model


@pytest.fixture
def asts_for_arithmetic() -> tuple[AST, AST]:
    return (AST.numeric(0.5 + 1j), AST.quantum_op("CNOT", (0,), (1,)))


@dataclass
class InputTypeTest:
    qubit_count: int
    directives: dict[str, Any]
    settings: dict[str, Any]
    ast: AST


class IRBuilderTest(IRBuilder[InputTypeTest]):
    @staticmethod
    def set_register(input_obj: InputTypeTest) -> AllocQubits:
        return AllocQubits(input_obj.qubit_count)

    @staticmethod
    def set_directives(input_obj: InputTypeTest) -> Attributes:
        return input_obj.directives

    @staticmethod
    def settings(input_obj: InputTypeTest) -> Attributes:
        return input_obj.settings

    @staticmethod
    def parse_sequence(input_obj: InputTypeTest) -> AST:
        return input_obj.ast


@pytest.fixture
def builder() -> IRBuilderTest:
    return IRBuilderTest()
