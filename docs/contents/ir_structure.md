# IR Structure
The main idea for Qadence 2 IR is to provide an abstract neutral atom device model.

Neutral atom devices usually rely on absolute values like laser power, atomic spacing in micrometers, and nanosecond pulse duration. Since the interaction between atoms and, therefore, the execution of algorithms in such devices are heavily influenced by those parameters, having a well-tuned algorithm for a specific device is desired. With that in mind, the IR definition should be independent of device-specific parameters, leaving their implementation to the backend. At the same time, the front-end compilation pipeline must build the IR from the algorithm and bridges with the backend at the low-level compilation pipeline, accessing its runtime resources.

Analog-relevant data such as the qubit register, parametric symbols and quantum instructions are wrapped in the IR, enabling each backend to handle them case-by-case. In particular, the instructions will provide only minimal information, such as the qubit support and the instruction label, i.e., which quantum operator or instruction is being applied, and the backend must provide some implementation for it.

The IR Model is split in four sections:

- Inputs
- Instructions
- Register
- Directives

The *Inputs* section is responsible for declaring the classical data and flagging them as trainable or not. This information is desired to ensure that only the parameters used in the machine learning training steps are considered for differentiability.

The *Instruction* section holds the sequence of classical computation via static single-assignment to avoid duplicate computation and help the differentiability instructions.

Quantum operations are passed as labels instead of fixed primitives (see the Challenges section). The IR definition is independent of device-specific parameters and leaves their configuration to the compiler, which builds an IR algorithm into instructions that contain the device-specific parameters.

The *Register* section holds either an abstract description of how the atoms are placed on the register or a connectivity graph, depending on the type of algorithm. Algorithms that don’t require customized registers are allowed to pass only the number of qubits. This process is delegated to the backend compiler to decide the best strategies to organize the atoms whenever possible.

The *Directives* section holds other device critical information for resource allocation like SLM mask target for individual qubit addressability.

Resource allocation, such as Registers and Directives, is usually not expected in an intermediate representation. However, as described before, those elements can affect algorithm design and pulse execution. The Challenges section presents more details about them.
