# Qadence Intermediate Representation (IR)

!!! note
    Qadence 2 IR is currently a *work in progress* and is under active development. Please be aware that the software is in an early stage, and frequent updates, including breaking changes, are to be expected. This means that:
    * Features and functionalities may change without prior notice.
    * The codebase is still evolving, and parts of the software may not function as intended.
    * Documentation and user guides may be incomplete or subject to significant changes.

Qadence 2 IR specifies an intermediate representation for Qadence 2. Front-ends, like [Qadence 2 Expressions](https://github.com/pasqal-io/qadence2-expressions), can compile to the IR and backends, like [Pulser](http://github.com/pasqal-io/pulser) or [PyQTorch](https://github.com/pasqal-io/pyqtorch) can be targeted from the IR using [Qadence 2 Platforms](https://github.com/pasqal-io/qadence-platforms).

## Installation

!!! note
    It is advised to set up a python environment before installing the package, such as [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments), [hatch](https://hatch.pypa.io/latest/), [pyenv](https://github.com/pyenv/pyenv), [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) or [poetry](https://python-poetry.org/). (Qadence 2 IR in development mode uses `hatch`).

To install the current version of Qadence 2 IR, there are a few options:

### 1. Installation from PYPI

On the terminal, type

```bash
pip install qadence2-ir
```

### 2. Installation from Source

Clone this repository by typing on the terminal

```bash
git clone https://github.com/pasqal-io/qadence2-ir.git
```

Go to `qadence2-ir` folder and install it using [hatch](https://hatch.pypa.io/latest/)

```bash
hatch -v shell
```

Use hatch environment on your IDE or terminal to use the `qadence2-ir` package.

## Usage

Usage guidelines

## Documentation

Documentation guidelines

## Contributing

Before making a contribution, please review our [code of conduct](docs/getting_started/CODE_OF_CONDUCT.md).

- **Submitting Issues:** To submit bug reports or feature requests, please use our [issue tracker](https://github.com/pasqal-io/qadence2-ir/issues).
- **Developing in qadence:** To learn more about how to develop within `qadence2-ir`, please refer to [contributing guidelines](docs/getting_started/CONTRIBUTING.md).

## License

Qadence 2 IR is a free and open source software package, released under the Apache License, Version 2.0.
