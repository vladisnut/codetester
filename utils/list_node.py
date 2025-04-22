from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return str(linked_list_to_list(self))


def list_to_linked_list(values: Optional[list]) -> Optional[ListNode]:
    dummy_node = ListNode()
    current_node = dummy_node

    for val in values or []:
        current_node.next = ListNode(val)
        current_node = current_node.next

    return dummy_node.next


def linked_list_to_list(head: Optional[ListNode]) -> list:
    values = []
    while head:
        values.append(head.val)
        head = head.next

    return values
