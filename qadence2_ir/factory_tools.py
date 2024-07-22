# TODO:
# - [ ] docstrings
# - [ ] logic comments

from __future__ import annotations

from functools import reduce
from typing import Any, Callable, Iterable

from .irast import AST
from .types import Alloc, Assign, Call, Load, QuInstruct


def filter_ast(predicate: Callable[[AST], bool], ast: AST) -> Iterable[AST]:
    if predicate(ast):
        yield ast

    else:
        for arg in ast.args:
            if isinstance(arg, AST):
                for term in filter_ast(predicate, arg):
                    yield term


def flatten_ast(ast: AST) -> Iterable[AST]:
    for arg in ast.args:
        if isinstance(arg, AST):
            for term in flatten_ast(arg):
                yield term

    yield ast


def extract_inputs(ast: AST) -> dict[str, Alloc]:
    return reduce(variable_to_alloc, filter_ast(lambda x: x.is_input_variable, ast), {})


def variable_to_alloc(inputs: dict[str, Alloc], ast: AST) -> dict[str, Alloc]:
    if ast.is_input_variable and ast.head not in inputs:
        name = ast.head
        size = ast.args[0]
        trainable = ast.args[1]

        inputs[name] = Alloc(size, trainable, **ast.attrs)

    return inputs


def build_instructions(ast: AST) -> list[QuInstruct | Assign]:
    instructions: list[QuInstruct | Assign] = []
    _build_instructions_core(ast, {}, instructions)
    return instructions


def _build_instructions_core(
    ast: AST,
    mem: dict[AST, Load],
    instructions: list[QuInstruct | Assign],
    count: int = 0,
) -> tuple[Load | None, int]:
    if ast.is_sequence:
        for arg in ast.args:
            term, count = _build_instructions_core(arg, mem, instructions, count)

    elif ast.is_quantum_op:
        term, count = _build_quantum_instructions(ast, mem, instructions, count)

    else:
        term, count = _build_classical_instructions(ast, mem, instructions, count)

    return term, count


def _build_quantum_instructions(
    ast: AST,
    mem: dict[AST, Load],
    instructions: list[QuInstruct | Assign],
    count: int = 0,
) -> tuple[Any, int]:
    if ast.is_quantum_op:
        support = ast.args[0]
        args = []
        for arg in ast.args[1:]:
            term, count = _build_classical_instructions(arg, mem, instructions, count)
            if term:
                args.append(term)
        instructions.append(QuInstruct(ast.head, support, *args, **ast.attrs))

    return None, count


def _build_classical_instructions(
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

    if ast.is_binary_op or ast.is_callable:
        args = []
        for arg in ast.args:
            term, count = _build_classical_instructions(arg, mem, instructions, count)
            args.append(term)

        label = f"%{count}"
        instructions.append(Assign(label, Call(ast.head, *args)))
        count += 1

        term = Load(label)
        mem[ast] = term

        return term, count

    raise NotImplementedError
