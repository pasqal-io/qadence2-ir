# TODO:
# - [ ] docstrings
# - [ ] logic comments

from __future__ import annotations

from functools import reduce
from typing import Callable, Iterable

from .irast import AST
from .types import Alloc, Assign, Call, Load, QuInstruct, Support


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
    return reduce(to_alloc, filter_ast(lambda x: x.is_input_variable, ast), {})


def to_alloc(inputs: dict[str, Alloc], ast: AST) -> dict[str, Alloc]:
    if ast.is_input_variable and ast.head not in inputs:
        name = ast.head
        size = ast.args[0]
        trainable = ast.args[1]

        inputs[name] = Alloc(size, trainable, **ast.attrs)

    return inputs


def build_instructions(ast: AST) -> list[QuInstruct | Assign]:
    instructions, _, _ = reduce(lambda acc, x: to_instruct(x, *acc), flatten_ast(ast), ([], {}, 0))
    return instructions


def to_instruct(
    ast: AST, instructions: list[QuInstruct | Assign], mem: dict[AST, Load], count: int
) -> tuple[list[QuInstruct | Assign], dict[AST, Load], int]:
    if ast in mem or ast.is_numeric or ast.is_sequence:
        return instructions, mem, count
    
    if ast.is_input_variable:
        mem[ast] = Load(ast.head)
        return instructions, mem, count
    
    args = []
    for arg in ast.args:
        if isinstance(arg, AST):
            if arg.is_numeric:
                args.append(arg.args[0])
            else:
                args.append(mem[arg])

        elif isinstance(arg, Support):
            args.append(arg)

    if ast.is_binary_op or ast.is_commutative_binary_op or ast.is_callable:
        label = f"%{count}"
        instructions.append(Assign(label, Call(ast.head, *args)))
        mem[ast] = Load(label)
        count += 1

    else:
        instructions.append(QuInstruct(ast.head, *args, **ast.attrs))

    return instructions, mem, count
