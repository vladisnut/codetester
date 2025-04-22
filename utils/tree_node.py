from itertools import islice
from queue import Queue
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return str(binary_tree_to_list(self))


def list_to_binary_tree(values: Optional[list]) -> Optional[TreeNode]:
    if not values:
        return None

    root = TreeNode(values[0])
    nodes = Queue()
    nodes.put((root, 'left'))
    nodes.put((root, 'right'))

    for val in islice(values, 1, None):
        node, direction = nodes.get()
        if val is not None:
            new_node = TreeNode(val)
            setattr(node, direction, new_node)

            nodes.put((new_node, 'left'))
            nodes.put((new_node, 'right'))

    return root


def binary_tree_to_list(root: Optional[TreeNode]) -> list:
    values = []
    nodes = Queue()
    nodes.put(root)

    while nodes.qsize():
        node = nodes.get()
        if node:
            values.append(node.val)
            nodes.put(node.left)
            nodes.put(node.right)
        else:
            values.append(None)

    while values and not values[-1]:
        values.pop()

    return values
