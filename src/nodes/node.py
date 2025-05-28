from abc import abstractmethod
from typing import Optional, Sequence, Type


class Node:
    ALT_NAME: str = None

    def __repr__(self):
        return str(self.to_list())

    def __eq__(self, other: "Node"):
        return self.to_list() == other.to_list()

    @abstractmethod
    def to_list(self) -> list:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_list(cls, values: Sequence) -> Optional["Node"]:
        raise NotImplementedError()


def get_node_classes() -> list[Type[Node]]:
    return Node.__subclasses__()
