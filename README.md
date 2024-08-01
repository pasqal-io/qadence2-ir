# Qadence 2 IR

Qadence 2 Intermediate Representation (IR) components.

### Example digital input.
```python
Model(
    register = AllocQubits(2),
    inputs = {
        "x": Alloc(1, trainable=True), 
    },
    instrunctions = [
        Assign("%0", Call("mul", 0.5, Load("x"))),
        QuInstruction("rx", Support(target=(0,)), Load("%0")),
        QuInstruction("x", Support(target=(1,), control=(0,))),
    ],
    directives = { # QPU options
    },
    settings = { # Other options
        "dtype": "f32",
    },
)
```

### Example analog input.
```python
Model(
    register = AllocQubits(
        num_qubits = 4,
        qubits_positions = [
            (-2, 1), (-1, 0), (0, 0), (1, -1)
        ],
        grid_type = "triangular",
        options = {
            "dmm": {
                "target_qubits": [0, 1],
                "weights": [0.5, 1.0],
            }
        }
    ),
    inputs = {
        # Inputs for a modulated pulse with 
        # trainable amplitude and detuning.
        "duration": Alloc(1, trainable=False),
        "omega": Alloc(4, trainable=True),
        "delta": Alloc(3, trainable=True),
    },
    instrunctions = [
        QuInstruct(
            "dyn_pulse",
            Support.target_all(),
            Load("duration"),
            Load("omega"),
            Load("delta"),
            0.0,  # phase
        ),
        QuInstruction(
            "dyn_local_phase",
            Support(target=(0, 1)),  # match with dmm
            duration = 1.2,
            concurrent = True,  # starts with the previous pulse
        ),
    ],
    directives = { # QPU options
        "virtual_device": {
            "rydberg_level": 65,
            "max_amplitude": 5.5,
            "max_abs_detuning": 70.0,
        }
    },
    settings = {},
)
```

### Example digital-analog input.
```python
Model(
    register = AllocQubits(
        num_qubits = ,
        qubits_positions = [],

    ),
    inputs = {

    },
    instrunctions = [
    ],
    directives = {},
    settings = {},
)
```

## Installation
Installation guidelines

## Usage
Usage guidelines

## Documentation
Documentation guidelines

## Contribute
Contribution guidelines
