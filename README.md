# Qadence 2 IR

Qadence 2 Intermediate Representation (IR) components.

### Example digital input.
```python
Model(
    register = AllocQubits(2),
    directives = { # for QPU options
    },
    settings = { # for building options
        "dtype": "f32",
    },
    inputs = {
        "x": Alloc(1, trainable=True), 
    },
    instrunctions = [
        
        # data encoding
        Assign("%0", Call("mul", 0.5, Load("x"))),
        QuInstruction("rx", Support(target=(0,)), Load("%0")),
        
        # cnot
        QuInstruction("x", Support(target=(1,), control=(0,))),
    ],
)
```

### Example digital-analog input.
```python
Model(
    register = AllocQubits(4),
    directives = {
        "dmm": {
            "targets": [0, 1, 2, 3],
            "weights": "from_inputs",
        }
    },
    settings = {},
    inputs = {
        "theta": Alloc(4, trainable=False)
        "duration": Alloc(1, trainable=True, attrs={"time_parameter": True})
        "omega": Alloc(5, trainable=True)
    },
    instrunctions = [
        # Tower feature map
        Assign("%0", Call("mul", 0.31831, Load("theta")),
        QuInstruct("set_dmm", Support.target_all(), Load("%0"))
        QuInstruct("rx", Support.target_all(), 1.570796),
        QuInstruct("dyn_local_pulse", Support.target_all(), attrs={"2pi_duration": True}),
        QuInstruct("rx", Support.target_all(), -1.570796),
        
        # Entanglement
        QuInstruct("dyn_interact", Support.target_all(), 2.5),
        
        # Trainable layer
        QuInstruct("dyn_pulse", Support.target_all(), Load("duration"), Load("omega"), 0.0, 0.0),
    ],
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

        # optional parameters
        grid_type = "triangular",
        grid_scale = 1.0,

        # Extra options
        options = {
            "multiplex": "max"
        }
    ),
    directives = { # for QPU options

        "rydberg_level": 65,
        "max_amplitude": 5.5,
        "max_abs_detuning": 70.0,

        "dmm": {
            "targets": [0, 3],
            "weights": [0.5, 1.0],
        }
    },
    settings = {  # for building options
        "prioritize_speed": True,
    },
    inputs = {
        "duration": Alloc(1, trainable=False, attrs={"time_parameter": True}),
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
            Support(target=(0, 1)),  # match with dmm targets
            attrs={
                "concurrent": True,  # starts with the previous pulse
                "duration": 1.2,
            }
        ),
    ],
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
