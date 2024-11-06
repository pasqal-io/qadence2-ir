from __future__ import annotations

import pytest

from qadence2_ir import AST


def test_numeric() -> None:
    ast = AST.numeric(0)
    assert ast._tag == ast.Tag.Numeric
    assert ast._head == ""
    assert ast._args == (0,)
    assert ast.attrs == dict()


def test_input_variable() -> None:
    ast = AST.input_variable("my-var", 1, True, attr1="value")
    assert ast._tag == ast.Tag.InputVariable
    assert ast._head == "my-var"
    assert ast._args == (1, True)
    assert ast._attrs == {"attr1": "value"}


def test_callable() -> None:
    ast = AST.callable("my-func", 2, "magic")
    assert ast._tag == ast.Tag.Call
    assert ast._head == "my-func"
    assert ast._args == (2, "magic")


def test_support() -> None:
    ast = AST.support((0, 1), (2, 3))
    assert ast._tag == ast.Tag.Support
    assert ast._head == ""
    assert ast._args == ((0, 1), (2, 3))


def test_quantum_op() -> None:
    ast = AST.quantum_op("CNOT", (0,), (1,), "arg1", kwarg1=8, kwarg2="my-compiler-flag")
    assert ast._tag == ast.Tag.QuantumOperator
    assert ast._head == "CNOT"
    assert ast._args == (AST.support((0,), (1,)), "arg1")
    assert ast._attrs == {"kwarg1": 8, "kwarg2": "my-compiler-flag"}


def test_sequence() -> None:
    operators = [AST.quantum_op("RX", (), ()), AST.quantum_op("CNOT", (0,), (1,))]
    ast = AST.sequence(*operators)
    assert ast._tag == ast.Tag.Sequence
    assert ast._head == ""
    assert ast._args == (*operators,)
    assert ast._attrs == dict()


@pytest.mark.parametrize(
    ["operation", "predicate"],
    [
        ("add", "is_addition"),
        ("sub", "is_subtraction"),
        ("mul", "is_multiplication"),
        ("div", "is_division"),
        ("pow", "is_power"),
    ],
)
def test_add(asts_for_arithmetic: tuple[AST, AST], operation: str, predicate: str) -> None:
    func = getattr(AST, operation)
    ast = func(*asts_for_arithmetic)
    assert ast._tag == ast.Tag.Call
    assert ast._head == operation
    assert ast._args == (*asts_for_arithmetic,)
    assert ast._attrs == dict()
    assert getattr(ast, predicate)
