from __future__ import annotations

import pytest

from qadence2_ir import AST


def test_numeric() -> None:
    ast = AST.numeric(0)
    assert ast.tag == ast.Tag.Numeric
    assert ast._head == ""
    assert ast._args == (0,)
    assert ast.attrs == dict()
    assert ast.is_numeric


def test_input_variable() -> None:
    ast = AST.input_variable("my-var", 1, True, attr1="value")
    assert ast.tag == ast.Tag.InputVariable
    assert ast._head == "my-var"
    assert ast._args == (1, True)
    assert ast._attrs == {"attr1": "value"}
    assert ast.is_input_variable


def test_callable() -> None:
    ast = AST.callable("my-func", 2, "magic")
    assert ast.tag == ast.Tag.Call
    assert ast._head == "my-func"
    assert ast._args == (2, "magic")
    assert ast.is_callable


def test_support() -> None:
    ast = AST.support((0, 1), (2, 3))
    assert ast.tag == ast.Tag.Support
    assert ast._head == ""
    assert ast._args == ((0, 1), (2, 3))
    assert ast.is_support


def test_quantum_op() -> None:
    ast = AST.quantum_op("CNOT", (0,), (1,), "arg1", kwarg1=8, kwarg2="my-compiler-flag")
    assert ast.tag == ast.Tag.QuantumOperator
    assert ast._head == "CNOT"
    assert ast._args == (AST.support((0,), (1,)), "arg1")
    assert ast._attrs == {"kwarg1": 8, "kwarg2": "my-compiler-flag"}
    assert ast.is_quantum_op


def test_sequence() -> None:
    operators = [AST.quantum_op("RX", (), ()), AST.quantum_op("CNOT", (0,), (1,))]
    ast = AST.sequence(*operators)
    assert ast.tag == ast.Tag.Sequence
    assert ast._head == ""
    assert ast._args == (*operators,)
    assert ast._attrs == dict()
    assert ast.is_sequence


@pytest.mark.parametrize(
    ["operation", "predicate"],
    [
        ("add", "is_addition"),
        ("sub", "is_subtraction"),
        ("mul", "is_multiplication"),
        ("div", "is_division"),
        ("rem", "is_remainder"),
        ("pow", "is_power"),
    ],
)
def test_add(asts_for_arithmetic: tuple[AST, AST], operation: str, predicate: str) -> None:
    func = getattr(AST, operation)
    ast = func(*asts_for_arithmetic)
    assert ast.tag == ast.Tag.Call
    assert ast._head == operation
    assert ast._args == (*asts_for_arithmetic,)
    assert ast._attrs == dict()
    assert getattr(ast, predicate)


def test_eq() -> None:
    # Not an ATS object
    assert AST.numeric(2.0).__eq__(2.0) is NotImplemented
    # Same tag and head
    assert AST.numeric(2) == AST.numeric(2)
    # Same tag and head but different args
    assert AST.callable("my-func", 9, 4) != AST.callable("my-func", 8, 2)
    # Same tag and head but different kwargs
    assert AST.input_variable("my-var", 1, True, kwarg=8) != AST.input_variable(
        "my-var", 1, True, kwarg=2
    )
    # Different tag
    assert AST.numeric(2) != AST.support((), ())
    # Multiplication and addition in different order
    assert AST.mul(AST.numeric(4), AST.numeric(2)) == AST.mul(AST.numeric(2), AST.numeric(4))
    assert AST.add(AST.numeric(4), AST.numeric(2)) == AST.add(AST.numeric(2), AST.numeric(4))


def test_repr() -> None:
    ast = AST.input_variable("my-var", 8, False, kwarg1=3, kwarg2="value")
    expected = "Tag.InputVariable('my-var', 8, False, kwarg1=3, kwarg2='value')"
    assert repr(ast) == expected
