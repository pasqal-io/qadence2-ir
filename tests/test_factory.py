from __future__ import annotations

from qadence2_ir import AST, AllocQubits, ir_compiler_factory
from qadence2_ir.types import Alloc, Assign, Call, Load, Model, QuInstruct, Support

from .conftest import InputTypeTest, IRBuilderTest


def test_init(quantum_ast: AST, builder: IRBuilderTest) -> None:
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
