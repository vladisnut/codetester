from collections.abc import Sequence
from typing import Any

from src.nodes.node import Node


class ListNode(Node):
    """
    Класс односвязного списка из LeetCode.
    """

    ALT_NAME = "ListNode"

    def __init__(self, val: Any = None, next: "ListNode | None" = None):
        self.val = val
        self.next = next

    def to_list(self) -> list:
        values = []
        node = self

        while node:
            values.append(node.val)
            node = node.next

        return values

    @classmethod
    def from_list(cls, values: Sequence) -> "ListNode | None":
        dummy_node = ListNode()
        current_node = dummy_node

        for val in values or []:
            current_node.next = ListNode(val)
            current_node = current_node.next

        return dummy_node.next
