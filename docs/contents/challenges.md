# Challenges

As pointed out above, digital and analog algorithms diverge in how they handle register topology. Contrary to classical computing, where the resource allocation can be left to the OS to control, the quantum resources must be explicit in analog quantum computation.

For digital devices and circuit-based algorithms, the register topology is important mostly during the compilation phase to reduce the number of SWAP gates applied. Analog algorithms and devices, on the other hand, rely on the topology to ensure the proper interaction between qubits regarding connectivity and strength. That led us to consider including the abstract representation of the register (either by unitless coordinates or connectivity graph) as part of the IR.

However, register preparation doesn’t represent an instruction in the sense of runtime since it needs to be loaded before the sequence starts and (for analog algorithms) cannot be changed during execution. Even if shuttling is available, the initial register configuration needs to be known to properly evaluate the atoms’ movement since such action will affect the connectivity of the register.

Besides the register, other elements like the SLM used to target individual qubits are part of the “booting”/resources allocation that is not directly connected to the register but cannot be addressed as regular instructions. Still, its presence may affect the behavior of specific pulses, which motivated the inclusion of a “Directives” section on the IR.

Primitive operations are another challenge in neutral atoms. The analog nature of the algorithms and device makes it difficult to clearly define “primitive operations”. Elementary structures like a pulse corresponding to the neutral atom Hamiltonian and an idle/wait instruction to let the qubits interact under free coupling (without drive).

To avoid define a fixed set of operations that may not reflect the hardware capabilities and to avoid constant changes in the IR definition to include new primitives, the instructions’ names are passed as labels like `QuInstrunct("dyn_pulse",…)` and `QuInstruct("rx".…)` instead of `Pulse(…)` and `RX(…)`. This may change in the future. However, right now, this flexibility allows us to explore the hardware's capabilities without being held by a particular set of instructions.
