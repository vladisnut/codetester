from collections import deque
from collections.abc import Sequence
from typing import Any

from src.nodes.node import Node


class BinaryTreeNode(Node):
    """
    Класс бинарного дерева из LeetCode.
    """

    ALT_NAME = "TreeNode"

    def __init__(
        self,
        val: Any = None,
        left: "BinaryTreeNode | None" = None,
        right: "BinaryTreeNode | None" = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    def to_list(self) -> list:
        values = []
        nodes = deque()
        nodes.append(self)

        while nodes:
            node = nodes.popleft()
            if node:
                values.append(node.val)
                nodes.append(node.left)
                nodes.append(node.right)
            else:
                values.append(None)

        while values and values[-1] is None:
            values.pop()

        return values

    @classmethod
    def from_list(cls, values: Sequence) -> "BinaryTreeNode | None":
        if not values:
            return None

        root = cls(values[0])
        nodes = deque()
        nodes.append((root, "left"))
        nodes.append((root, "right"))

        for value in values[1:]:
            node, direction = nodes.popleft()

            if value is not None:
                new_node = cls(value)
                setattr(node, direction, new_node)

                nodes.append((new_node, "left"))
                nodes.append((new_node, "right"))

        return root
