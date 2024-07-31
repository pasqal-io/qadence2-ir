from __future__ import annotations

from typing import Callable

from .factory_tools import build_instructions, extract_inputs
from .irast import InputType
from .irbuilder import AbstractIRBuilder as IRBuilder
from .types import Model


def ir_compiler_factory(builder: IRBuilder[InputType]) -> Callable[[InputType], Model]:
    """Use an IRBuilder[InputType] to create an IR compiler function that converts
    an input of type `InputType` and returns a Model.

    By convention, the IR compiler should be named as `compile_to_model`.
    """

    def ir_compiler(input_obj: InputType) -> Model:
        register = builder.set_register(input_obj)
        directives = builder.set_directives(input_obj)
        settings = builder.settings(input_obj)

        ast = builder.parse_sequence(input_obj)
        inputs = extract_inputs(ast)
        instructions = build_instructions(ast)

        return Model(register, inputs, instructions, directives, settings)

    return ir_compiler
