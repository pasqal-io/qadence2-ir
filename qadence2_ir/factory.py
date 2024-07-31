from __future__ import annotations

from typing import Callable

from .factory_tools import build_instructions, extract_inputs_variables
from .irast import InputType
from .irbuilder import IRBuilder
from .types import Model


def ir_compiler_factory(builder: IRBuilder[InputType]) -> Callable[[InputType], Model]:
    """Use an IRBuilder[InputType] to create an IR compiler function that converts an input of type
    `InputType` and returns a Model.

    The IR compiler must be named 'compile_to_model' by convention to ensure accessibility to other
    engines in the framework.

    Arguments:
        - builder: A concrete implementation of the generic class `IRBuilder` for a particular
            `InputType`.
    
    Return:
        A function that compiles an `InputType` object to the Qadence-IR (`Model`).
    """

    def ir_compiler(input_obj: InputType) -> Model:
        register = builder.set_register(input_obj)
        directives = builder.set_directives(input_obj)
        settings = builder.settings(input_obj)

        ast = builder.parse_sequence(input_obj)
        input_variables = extract_inputs_variables(ast)
        instructions = build_instructions(ast)

        return Model(register, input_variables, instructions, directives, settings)

    return ir_compiler
