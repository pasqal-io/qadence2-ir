from __future__ import annotations

from qadence2_ir.factory_tools import (
    build_instructions,
    extract_inputs_variables,
    filter_ast,
    flatten_ast,
    to_alloc,
    to_instruct,
)
from qadence2_ir.irast import AST
from qadence2_ir.types import Alloc, Assign, Call, Load, QuInstruct, Support


def test_filter_ast(classical_ast: AST) -> None:
    # Flat ast
    x = AST.input_variable("x", 1, False)
    assert [x] == list(filter_ast(lambda ast: ast.is_input_variable, x))
    assert [] == list(filter_ast(lambda ast: ast.is_callable, x))

    # Nested ast
    assert list(filter_ast(lambda x: x.is_input_variable, classical_ast)) == [x, x]
    nested_ast = AST.callable("div", AST.numeric(8), AST.numeric(3))
    expected = [AST.numeric(8), AST.numeric(3)]
    assert expected == list(filter_ast(lambda ast: ast.is_numeric, nested_ast))


def test_flatten_ast(classical_ast: AST) -> None:
    x = AST.input_variable("x", 1, False)
    three = AST.numeric(3)
    div = AST.div(x, three)
    fn = AST.callable("fn", div, x)

    res = list(flatten_ast(classical_ast))
    assert res == [x, three, div, x, fn]


def test_extract_inputs(classical_ast: AST, quantum_ast: AST) -> None:
    expected = {"x": Alloc(1, False)}
    res = extract_inputs_variables(classical_ast)
    assert res == expected
    res2 = extract_inputs_variables(classical_ast)
    assert res2 == expected


def test_to_alloc() -> None:
    ast = AST.input_variable("x", 1, False)
    inputs = {"x": Alloc(1, False)}
    # Test if added to inputs
    assert to_alloc({}, ast) == inputs
    # Test if not added twice
    assert to_alloc(inputs, ast) == inputs
    # Test if not input variable
    assert to_alloc({}, AST.callable("my-func")) == {}


def test_build_instructions(quantum_ast: AST) -> None:
    res = build_instructions(quantum_ast)
    target = [
        Assign("%0", Call("div", Load("x"), 3.0)),
        Assign("%1", Call("fn", Load("%0"), Load("x"))),
        QuInstruct("rx", Support(target=(0,), control=(1,)), Load("%1")),
    ]
    assert res == target


def test_to_instruct() -> None:
    assert to_instruct(AST.numeric(3), [], {}, 0) == ([], {}, 0)
    assert to_instruct(AST.support((0,), (1,)), [], {}, 0) == ([], {}, 0)
    assert to_instruct(AST.sequence(AST.quantum_op("X", (0,), ())), [], {}, 0) == ([], {}, 0)

    ast_input_var = AST.input_variable("my-var", 1, True)
    expected_input_var: tuple[list, dict[AST, Load], int] = ([], {ast_input_var: Load("my-var")}, 0)
    assert to_instruct(ast_input_var, [], {}, 0) == expected_input_var
    assert to_instruct(ast_input_var, [], expected_input_var[1], 0) == expected_input_var

    ast_callable = AST.callable("my-func", AST.numeric(2))
    assert to_instruct(ast_callable, [], {}, 0) == (
        [Assign("%0", Call("my-func", 2))],
        {ast_callable: Load("%0")},
        1,
    )

    ast_quantum_op = AST.quantum_op("X", (0,), (), "random_arg")
    assert to_instruct(ast_quantum_op, [], {}, 0) == ([QuInstruct("X", Support((0,), ()))], {}, 0)
