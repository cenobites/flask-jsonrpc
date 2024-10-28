from typing import Any

# Added in version 3.11.
from typing_extensions import Self


class EqMock:
    value: Any = None

    def __init__(self: Self, remember: bool = False) -> None:
        self.remember: bool = remember

    def __eq__(self: Self, other: Any) -> bool:  # noqa: ANN401
        if self.remember and self.value is not None:
            return self.value == other
        else:
            assert other, other

            if self.remember:
                self.value = other

        return True

    def __repr__(self: Self) -> str:
        return repr(self.value) if self.remember else super().__repr__()

    def __str__(self: Self) -> str:
        return str(self.value) if self.remember else super().__str__()
