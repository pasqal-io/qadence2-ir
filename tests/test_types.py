from __future__ import annotations

from qadence2_ir.types import Alloc, Assign


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
