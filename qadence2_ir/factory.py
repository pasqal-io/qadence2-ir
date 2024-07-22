# TODO:
# - [ ] docstrings

from __future__ import annotations

from typing import Callable

from .factory_tools import extract_inputs, extract_instructions
from .irast import InputType
from .irbuilder import AbstractIRBuilder
from .types import Model


def irc_factory(builder: AbstractIRBuilder) -> Callable[[InputType], Model]:  # type: ignore
    def ircompiler(input_obj: InputType) -> Model:
        register = builder.set_register(input_obj)
        directives = builder.set_directives(input_obj)
        settings = builder.settings(input_obj)

        ast = builder.parse_sequence(input_obj)
        inputs = extract_inputs(ast)
        instructions = extract_instructions(ast)

        return Model(register, inputs, instructions, directives, settings)

    return ircompiler
