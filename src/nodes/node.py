from abc import abstractmethod
from collections.abc import Sequence


class Node:
    ALT_NAME: str = None

    def __repr__(self):
        return str(self.to_list())

    def __eq__(self, other: "Node"):
        return self.to_list() == other.to_list()

    @abstractmethod
    def to_list(self) -> list:
        pass

    @classmethod
    @abstractmethod
    def from_list(cls, values: Sequence) -> "Node | None":
        pass


def get_nodes() -> list[type[Node]]:
    return Node.__subclasses__()
