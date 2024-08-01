from __future__ import annotations

from qadence2_ir.factory_tools import (
    build_instructions,
    extract_inputs_variables,
    filter_ast,
    flatten_ast,
)
from qadence2_ir.irast import AST
from qadence2_ir.types import Alloc, Assign, Call, Load, QuInstruct, Support


def test_flatten_ast(classical_ast: AST) -> None:
    x = AST.input_variable("x", 1, False)
    three = AST.numeric(3)
    div = AST.div(x, three)
    fn = AST.callable("fn", div, x)

    res = list(flatten_ast(classical_ast))
    assert res == [x, three, div, x, fn]


def test_filter_ast(classical_ast: AST) -> None:
    x = AST.input_variable("x", 1, False)

    res = list(filter_ast(lambda x: x.is_input_variable, classical_ast))
    assert res == [x, x]


def test_extract_inputs(classical_ast: AST) -> None:
    res = extract_inputs_variables(classical_ast)
    assert res == {"x": Alloc(1, False)}


def test_build_instructions(quantum_ast: AST) -> None:
    res = build_instructions(quantum_ast)
    target = [
        Assign("%0", Call("div", Load("x"), 3.0)),
        Assign("%1", Call("fn", Load("%0"), Load("x"))),
        QuInstruct("rx", Support(target=(0,), control=(1,)), Load("%1")),
    ]
    assert res == target
