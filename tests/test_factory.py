from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qadence2_ir import AST, AllocQubits, Attributes, IRBuilder, ir_compiler_factory
from qadence2_ir.types import Alloc, Assign, Call, Load, Model, QuInstruct, Support


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


def test_init(quantum_ast: AST) -> None:
    builder = IRBuilderTest()
    ir_compiler = ir_compiler_factory(builder)
    input_ = InputTypeTest(10, {"my-directive": False}, {"my-setting": 8}, quantum_ast)
    model = ir_compiler(input_)
    expected = Model(
        AllocQubits(10),
        {"x": Alloc(1, False)},
        [
            Assign("%0", Call("div", Load("x"), 3)),
            Assign("%1", Call("fn", Load("%0"), Load("x"))),
            QuInstruct("rx", Support((0,), (1,)), Load("%1")),
        ],
        {"my-directive": False},
        {"my-setting": 8},
    )
    assert model == expected
