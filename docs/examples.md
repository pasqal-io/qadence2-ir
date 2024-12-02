## Examples
The following examples were generate to present some possible algorithms and may not be
fully implementable in the hardware at the moment.

### Example digital input.
```python
Model(
    register = AllocQubits(2),
    directives = { # for QPU options
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
            "weights": "equal",
        }
    },
    settings = {},
    inputs = {
        "theta": Alloc(4, trainable=False)
        "duration": Alloc(1, trainable=True)
        "omega": Alloc(5, trainable=True)
    },
    instrunctions = [
        # Tower feature map
        Assign("%0", Call("mul", 0.31831, Load("theta")),
        QuInstruct("set_dmm", Support.target_all(), Load("%0"))
        QuInstruct("rx", Support.target_all(), 1.570796),
        QuInstruct("dyn_local_pulse", Support.target_all(), 2.0),
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
    ),
    directives = {
        "dmm": {
            "targets": [0, 3],
            "weights": [0.5, 1.0],
        }
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
            1.2,  # duration
            attrs={
                "concurrent": True,  # starts with the previous pulse
            }
        ),
    ],
)
```

### Example analog input (alternative)
This example is intend to be used with backends that either support crossing-lattice  or similar
algorithms, or gridless backends (e.g. PyQ).
```python
Model(
    register = AllocQubits(
        num_qubits = 4,
        connectivity = {
            (0, 1): 1.2,
            (0, 3): 0.9,
            (1, 2): 1.4,
            (2, 3): 2.1,
        }
    ),
    directives = {
        "dmm": {
            "targets": [0, 3],
            "weights": [0.5, 1.0],
        }
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

```python
Model(
    register=AllocQubits(
        num_qubits=3,
        connectivity={(0,1): 1., (0,2): .5, (1,2): .5},
    ),
    directives={
        "dmm": {"targets": [0, 1]}
    },
    inputs={
        't': Alloc(1, trainable=True)
    },
    instructions=[
        # The presence of the `dmm` allows a single qubit operation by
        # dynamic decoupling the others two qubits.
        QuInstruct('x', Support(target=(2,))),

        Assign('%0', Mul(1.57, Load('t')),
        QuInstruct('dyn_pulse', target_all(), Load('%0'), 1.0),
    ],
)
```