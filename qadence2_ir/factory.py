# TODO:
# - [ ] docstrings

from __future__ import annotations

from typing import Callable

from .factory_tools import build_instructions, extract_inputs
from .irast import InputType
from .irbuilder import AbstractIRBuilder
from .types import Model


def irc_factory(builder: AbstractIRBuilder) -> Callable[[InputType], Model]:
    def ir_compiler(input_obj: InputType) -> Model:
        register = builder.set_register(input_obj)
        directives = builder.set_directives(input_obj)
        settings = builder.settings(input_obj)

        ast = builder.parse_sequence(input_obj)
        inputs = extract_inputs(ast)
        instructions = build_instructions(ast)

        return Model(register, inputs, instructions, directives, settings)

    return ir_compiler
