from __future__ import annotations

from qadence2_ir.types import Alloc


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
    assert create_alloc().__eq__([]) is NotImplemented
