from node import Node
from typing import Callable, Generator, Self
from collections import deque

class Tree[T]:
    def __init__(self, root: Node[T]) -> None:
        self._root = root
        self._max_children = root.max_children
        if self._max_children is not None:
                if len(root.get_children()) > self._max_children:
                    raise ValueError(f"Node cannot have more than {self._max_children} children.")



    @property
    def root(self) -> Node[T]:
        return self._root
    
    @property
    def max_children(self) -> int | None:
        return self._max_children

    @max_children.setter
    def max_children(self, max_children: int | None) -> None:
        if max_children is not None:
            if max_children < 0:
                raise ValueError(f"Maximum number of children ({max_children}) must be a positive integer.")
        if len(self.children) > max_children:
            raise ValueError(f"The maximum number of children ({max_children}) cannot be less than the current number of children ({len(self.children)}).")
        self._max_children = max_children

    @classmethod
    def from_dict(cls, tree_as_dict: dict) -> Self[T]:
        root = Node.from_dict(tree_as_dict)
        return cls(root)
    
    def to_dict(self) -> dict:
        return self.root.to_dict()

    def preorder_traversal(self, node: Node[T], callback: Callable[[Node[T]], bool] | None = None) -> Generator[Node[T], None, None]:
        if callback is not None and not callback(node):
            return
        yield self
        for child in node.children:
            yield from child.preorder_traversal(callback)

    def postorder_traversal(self, node: Node[T], callback: Callable[[Node[T]], bool] | None = None) -> Generator[Node[T], None, None]:
        if callback is not None and not callback(node):
            return
        for child in node.children:
            yield from child.postorder_traversal(callback)
        yield self

    def levelorder_traversal(self, node: Node[T], callback: Callable[[Node[T]], bool] | None = None) -> Generator[Node[T], None, None]:
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if callback is not None and not callback(current):
                return
            yield current
            queue.extend(current.children)

    def upwards_traversal(self, node: Node[T], callback: Callable[[Node[T]], bool] | None = None) -> Generator[Node[T], None, None]:
        current = node
        while current is not None:
            if callback is not None and not callback(current):
                return
            yield current
            current = current.parent

    def lowest_common_ancestor(self, node1: Node[T], node2: Node[T]) -> Node[T]:
        return node1.lowest_common_ancestor(node2)
    
    def get_path(self, node1: Node[T], node2: Node[T]) -> list[Node[T]]:
        return node1.get_path(node2)
    
    def get_distance(self, node1: Node[T], node2: Node[T]) -> int:
        return node1.get_distance(node2)

    def get_subtree(self, node: Node[T]) -> Self[T]:
        for n in node.upwards_traversal():
            if n == self.root:
                return Tree(node)
        raise ValueError(f"The given node is not in this tree.")

    def contains_subtree(self, other: Self) -> bool:
        for node in self.levelorder_traversal():
            if node == other.root:
                return True
        return False
    
    def add_node(self, node: Node[T], parent: Node[T] = None) -> None:
        if not parent:
            parent = self.root
        parent.add_child(node)

    def add_nodes(self, nodes: list[Node[T]], parent: Node[T] = None) -> None:
        if not parent:
            parent = self.root
        parent.add_children(nodes)

    def remove_node(self, node: Node[T], parent: Node[T] = None) -> None:
        if parent:
            parent.remove_child(node)
        # which traversal algorithm is most efficient?
        for n in self.levelorder_traversal(self.root):
            if n == node.parent:
                n.remove_child(node)
                break