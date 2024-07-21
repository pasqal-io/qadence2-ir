# TODO:
# - [ ] docstrings
# - [ ] logic comments

from __future__ import annotations

from typing import Any

from .irast import AST
from .types import Alloc, Assign, QuInstruct, Load, Call


def extract_inputs(ast: AST) -> dict[str, Alloc]:
    inputs: dict[str, Alloc] = dict()
    _extract_inputs_core(ast, inputs)
    return inputs


def _extract_inputs_core(ast: AST, inputs: dict[str, Alloc]) -> None:
    if ast.is_numeric:
        return

    if ast.is_input_variable:
        name = ast.head
        size = ast.args[0]
        trainable = ast.args[1]

        inputs[name] = Alloc(size, trainable, **ast.attrs)

    else:
        for arg in ast.args:
            _extract_inputs_core(arg, inputs)


def extract_instructions(ast: AST) -> list[QuInstruct | Assign]:
    instructions: list[QuInstruct | Assign] = []
    _extract_instructions_core(ast, {}, instructions)
    return instructions


def _extract_instructions_core(
    ast: AST,
    mem: dict[AST, Load],
    instructions: list[QuInstruct | Assign],
    count: int = 0,
) -> tuple[Load | None, int]:
    if ast.is_sequence:
        for arg in ast.args:
            term, count = _extract_instructions_core(arg, mem, instructions, count)

    elif ast.is_quantum_op:
        term, count = _extract_quantum_instructions(ast, mem, instructions, count)

    else:
        term, count = _extract_classical_instructions(ast, mem, instructions, count)

    return term, count


def _extract_quantum_instructions(
    ast: AST,
    mem: dict[AST, Load],
    instructions: list[QuInstruct | Assign],
    count: int = 0,
) -> tuple[Any, int]:
    if ast.is_quantum_op:
        args = []
        for arg in ast.args:
            term, count = _extract_classical_instructions(arg, mem, instructions, count)
            if term:
                args.append(term)
        instructions.append(QuInstruct(ast.head, *args, **ast.attrs))

    return None, count


def _extract_classical_instructions(
    ast: AST,
    mem: dict[AST, Load],
    instructions: list[QuInstruct | Assign],
    count: int = 0,
) -> tuple[Load | None, int]:
    if ast in mem:
        return mem[ast], count

    if ast.is_numeric:
        return ast.args[0], count

    if ast.is_input_variable:
        return Load(ast.head), count

    if ast.is_binary_op:
        lhs, count = _extract_classical_instructions(
            ast.args[0], mem, instructions, count
        )
        rhs, count = _extract_classical_instructions(
            ast.args[1], mem, instructions, count
        )

        args = (lhs, rhs)

    if ast.is_callable:
        args = []
        for arg in ast.args:
            term, count = _extract_classical_instructions(arg, mem, instructions, count)
            args.append(term)

    label = f"%{count}"
    instructions.append(Assign(label, Call(ast.head, *args)))
    count += 1

    term = Load(label)
    mem[ast] = term

    return term, count
