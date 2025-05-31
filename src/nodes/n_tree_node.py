from collections import deque
from collections.abc import Sequence
from typing import Any

from src.nodes.node import Node


class NTreeNode(Node):
    """
    Класс N-дерева из LeetCode.
    """

    ALT_NAME = "Node"

    def __init__(self, val: Any = None, children: list["NTreeNode"] = None):
        self.val = val
        self.children = children or []

    def to_list(self) -> list:
        values = [self.val, None]
        nodes = deque()
        nodes.append(self)

        while nodes:
            node = nodes.popleft()
            for child in node.children or []:
                values.append(child.val)
                nodes.append(child)
            values.append(None)

        while values and values[-1] is None:
            values.pop()

        return values

    @classmethod
    def from_list(cls, values: Sequence) -> "NTreeNode | None":
        if not values:
            return None

        root = cls(values[0])
        nodes = deque()
        nodes.append(root)
        node = None

        for value in values[1:]:
            if value is None:
                node = nodes.popleft()
            else:
                if node.children is None:
                    node.children = []
                new_node = cls(value)
                node.children.append(new_node)
                nodes.append(new_node)

        return root
