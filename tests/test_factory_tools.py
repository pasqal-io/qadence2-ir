from __future__ import annotations

import unittest

from qadence2_ir.irast import AST
from qadence2_ir.factory_tools import build_instructions, extract_inputs, flatten_ast, filter_ast
from qadence2_ir.types import Alloc, Assign, Call, Load, QuInstruct, Support


class TestFactoryTools(unittest.TestCase):
    def test_flatten_ast(self) -> None:
        x = AST.input_variable("x", 1, False)
        three = AST.numeric(3)
        div = AST.binary_op("/", x, three)
        ast = AST.callable("fn", div, x)

        res = list(flatten_ast(ast))
        self.assertEqual(res, [x, three, div, x, ast])

    def test_filter_ast(self) -> None:
        x = AST.input_variable("x", 1, False)
        three = AST.numeric(3)
        div = AST.binary_op("/", x, three)
        ast = AST.callable("fn", div, x)

        res = list(filter_ast(lambda x: x.is_input_variable, ast))
        self.assertEqual(res, [x, x])

    def test_extract_inputs(self) -> None:
        x = AST.input_variable("x", 1, False)
        three = AST.numeric(3)
        div = AST.binary_op("/", x, three)
        ast = AST.callable("fn", div, x)

        res = extract_inputs(ast)
        self.assertEqual(res, {"x": Alloc(1, False)})

    def test_build_instructions(self) -> None:
        x = AST.input_variable("x", 1, False)
        three = AST.numeric(3.0)
        div = AST.binary_op("/", x, three)
        fn = AST.callable("fn", div, x)
        ast = AST.quantum_op("rx", (0,), (1,), fn)

        res = build_instructions(ast)
        target = [
            Assign("%0", Call("/", Load("x"), 3.0)),
            Assign("%1", Call("fn", Load("%0"), Load("x"))),
            QuInstruct("rx", Support(target=(0,), control=(1,)), Load("%1")),
        ]
        self.assertEqual(res, target)
