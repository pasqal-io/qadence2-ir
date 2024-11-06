# use this file for configuring test fixtures and
# functions common to every test
from __future__ import annotations

import pytest

from qadence2_ir.irast import AST


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
def asts_for_arithmetic() -> tuple[AST, AST]:
    return (AST.numeric(0.5 + 1j), AST.quantum_op("CNOT", (0,), (1,)))
