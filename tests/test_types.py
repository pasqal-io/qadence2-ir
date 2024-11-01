from __future__ import annotations

import pytest

from qadence2_ir.types import Alloc, Assign, Call, Load, Support


def test_alloc_repr() -> None:
    assert Alloc(1, True).__repr__() == "Alloc(1, trainable=True)"
    assert Alloc(6, False).__repr__() == "Alloc(6, trainable=False)"
    assert (
        Alloc(1, False, attr1=5, attr2=[5, 6, 3]).__repr__()
        == "Alloc(1, trainable=False, attrs={'attr1': 5, 'attr2': [5, 6, 3]})"
    )


def test_alloc_eq() -> None:
    def create_alloc() -> Alloc:
        return Alloc(3, True, attributes={"test": 8, "bla": (2, "str", 84.2)})

    assert create_alloc() == create_alloc()
    assert create_alloc() != Alloc(1, True)
    assert create_alloc() != Alloc(1, False)
    assert create_alloc().__eq__([]) is NotImplemented


def test_assign_repr() -> None:
    assert Assign("my-var", 8).__repr__() == "Assign('my-var', 8)"
    assert Assign("my-var", 3.14).__repr__() == "Assign('my-var', 3.14)"
    assert (
        Assign("var*with@non$standard123characters", [3, 2, 1]).__repr__()
        == "Assign('var*with@non$standard123characters', [3, 2, 1])"
    )


def test_assign_eq() -> None:
    assert Assign("x", 2) == Assign("x", 2)
    assert Assign("x", 2) != Assign("y", 2)
    assert Assign("x", 1) != Assign("x", 34)
    assert Assign("x", 5).__eq__({}) is NotImplemented


def test_load_repr() -> None:
    assert Load("my-var").__repr__() == "Load('my-var')"


def test_load_eq() -> None:
    assert Load("my-var") == Load("my-var")
    assert Load("x") != Load("y")
    assert Load("x") != "x"


def test_call_repr() -> None:
    assert Call("my-func").__repr__() == "Call('my-func')"
    assert Call("my-func", 9, "str").__repr__() == "Call('my-func', 9, 'str')"


def test_call_eq() -> None:
    assert Call("my-func") == Call("my-func")
    assert Call("my-func", 3) == Call("my-func", 3)
    assert Call("my-func") != Call("fibonaci")
    assert Call("my-func", 2) != Call("my-func", 4)
    assert Call("my-func", []) != Call("my-func", 4)


def test_support_init() -> None:
    only_target = Support((0,))
    assert only_target.target == (0,)
    assert only_target.control == ()

    with pytest.raises(TypeError):
        Support(control=(0,))  # type: ignore

    target_and_control = Support((2, 0), (1,))
    assert target_and_control.target == (2, 0)
    assert target_and_control.control == (1,)

    target_all = Support.target_all()
    assert target_all.target == ()
    assert target_all.control == ()


def test_support_repr() -> None:
    assert repr(Support((0,))) == "Support(target=(0,))"
    assert repr(Support((1,), (0,))) == "Support(target=(1,), control=(0,))"
    assert repr(Support(())) == "Support.target_all()"
    assert repr(Support.target_all()) == "Support.target_all()"


def test_support_eq() -> None:
    assert Support((0,)) == Support((0,))
    assert Support((0,), (1, 3)) == Support((0,), (1, 3))
    assert Support((0,)) != Support((1,))
    assert Support((0,), (1,)) != Support((0,))
    assert Support((0,), (1,)) != Support((0,), (3, 0))
    assert Support((3,)) != "Support((3,))"
