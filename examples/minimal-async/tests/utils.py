from typing import Any


class EqMock:
    value: Any = None

    def __init__(self, remember: bool = False) -> None:
        self.remember: bool = remember

    def __eq__(self, other: Any) -> bool:  # noqa: ANN401
        if self.remember and self.value is not None:
            return self.value == other
        else:
            assert other, other

            if self.remember:
                self.value = other

        return True

    def __repr__(self) -> str:
        return repr(self.value) if self.remember else super().__repr__()

    def __str__(self) -> str:
        return str(self.value) if self.remember else super().__str__()
