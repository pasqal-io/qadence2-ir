from __future__ import annotations

from functools import reduce
from typing import Callable, Iterable

from .irast import AST
from .types import Alloc, Assign, Call, Load, QuInstruct, Support


def filter_ast(predicate: Callable[[AST], bool], ast: AST) -> Iterable[AST]:
    """Filter the elements of the AST using the `predicate` function and return
    an iterable flattened version of the AST.

    >>> ast = AST.binar_op("/", AST.numeric(2), AST.callable("fn", AST.numeric(3)))
    >>> list(filter_ast(lambda x: x.is_numeric, ast))
    [AST.numeric(2), AST.numeric(3)]
    """

    if predicate(ast):
        yield ast

    else:
        for arg in ast.args:
            if isinstance(arg, AST):
                for term in filter_ast(predicate, arg):
                    yield term


def flatten_ast(ast: AST) -> Iterable[AST]:
    """Returns an interable flattened version of the AST. The arguments of
    operations/functions are kept before the operation/function.

    >>> ast = AST.binar_op("/", AST.numeric(2), AST.callable("fn", AST.numeric(3)))
    >>> list(flatten_ast(ast))
    [
        AST.numeric(2),
        AST.numeric(3),
        AST.callable("fn", AST.numeric(3)),
        AST.binar_op("/", AST.numeric(2), AST.callable("fn", AST.numeric(3))),
    ]
    """

    for arg in ast.args:
        if isinstance(arg, AST):
            for term in flatten_ast(arg):
                yield term

    yield ast


def extract_inputs(ast: AST) -> dict[str, Alloc]:
    """Convert all the input variables in the AST into allocation instructions."""

    return reduce(to_alloc, filter_ast(lambda x: x.is_input_variable, ast), dict())


def to_alloc(inputs: dict[str, Alloc], ast: AST) -> dict[str, Alloc]:
    """If the `ast` is an input variable, add it to the inputs to be allocated
    if not present yet.
    """

    if ast.is_input_variable and ast.head not in inputs:
        name = ast.head
        size = ast.args[0]
        trainable = ast.args[1]

        inputs[name] = Alloc(size, trainable, **ast.attrs)

    return inputs


def build_instructions(ast: AST) -> list[QuInstruct | Assign]:
    """Converts a sequence of instructions in the AST form into a list of Model
    instructions.
    """

    instructions, _, _ = reduce(  # type: ignore
        lambda acc, x: to_instruct(x, *acc), flatten_ast(ast), ([], dict(), 0)  # type: ignore
    )
    return instructions


def to_instruct(
    ast: AST,
    instructions_list: list[QuInstruct | Assign],
    memoise: dict[AST, Load],
    single_assign_index: int,
) -> tuple[list[QuInstruct | Assign], dict[AST, Load], int]:
    """Add the `ast` to the `instructions_list` if `ast` is a classical function
    or a quantum instruction.

    When the `ast` is a classical function, it uses the `single_assign_index` to
    assign the call to a temporary variable using memoisation to avoid duplicated
    assignments.
    """

    if ast in memoise or ast.is_numeric or ast.is_support or ast.is_sequence:
        return instructions_list, memoise, single_assign_index

    if ast.is_input_variable:
        memoise[ast] = Load(ast.head)
        return instructions_list, memoise, single_assign_index

    args = []
    for arg in ast.args:
        if isinstance(arg, AST):
            if arg.is_numeric:
                args.append(arg.args[0])
            elif arg.is_support:
                args.append(Support(target=arg.args[0], control=arg.args[1]))
            else:
                args.append(memoise[arg])

    if ast.is_binary_op or ast.is_commutative_binary_op or ast.is_callable:
        label = f"%{single_assign_index}"
        instructions_list.append(Assign(label, Call(ast.head, *args)))
        memoise[ast] = Load(label)
        single_assign_index += 1

    else:
        instructions_list.append(QuInstruct(ast.head, *args, **ast.attrs))

    return instructions_list, memoise, single_assign_index
