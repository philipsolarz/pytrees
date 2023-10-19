from node import Node
from typing import Callable, Generator, Self
from collections import deque
from enum import Enum

class TraversalType(Enum):
    PREORDER = "preorder"
    POSTORDER = "postorder"
    LEVELORDER = "levelorder"
    UPWARDS = "upwards"

class Tree[T]:
    def __init__(self, root: Node[T]) -> None:
        self._root = root
        self._max_children = root.max_children
        if self._max_children is not None:
                if len(root.get_children()) > self._max_children:
                    raise ValueError(f"Node cannot have more than {self._max_children} children.")
        self._default_traversal_type = TraversalType.PREORDER
                
    def __eq__(self, other: Self[T]) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return self.contains_subtree(other) and other.contains_subtree(self)

    def __lt__(self, other: Self[T]) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return other.contains_subtree(self) and not self.__eq__(other)

    def __le__(self, other: Self[T]) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return other.contains_subtree(self)

    def __gt__(self, other: Self[T]) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return self.contains_subtree(other) and not self.__eq__(other)

    def __ge__(self, other: Self[T]) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return self.contains_subtree(other)

    def __ne__(self, other: Self[T]) -> bool:
        return not self.__eq__(other)
    
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

    @property
    def default_traversal_type(self) -> TraversalType:
        return self._default_traversal_type
    
    @default_traversal_type.setter
    def default_traversal_type(self, traversal_type: TraversalType) -> None:
        self._default_traversal_type = traversal_type

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

    def size(self) -> int:
        return len(list(self.levelorder_traversal(self.root)))
    
    def depth(self, node: Node[T]) -> int:
        return len(list(self.upwards_traversal(node))) - 1
    
    def find(self, query_function: Callable[[Node[T]], bool], traversal_type: TraversalType | None = None) -> Node[T] | None:
        if traversal_type is None:
            traversal_type = self.default_traversal_type

        if traversal_type == TraversalType.PREORDER:
            return self._find_preorder(query_function)
        elif traversal_type == TraversalType.POSTORDER:
            return self._find_postorder(query_function)
        elif traversal_type == TraversalType.LEVELORDER:
            return self._find_levelorder(query_function)
        elif traversal_type == TraversalType.UPWARDS:
            return self._find_upwards(query_function)
        
    def _find_preorder(self, query_function: Callable[[Node[T]], bool]) -> Node[T] | None:
        for node in self.preorder_traversal(self.root):
            if query_function(node):
                return node
        return None
    
    def _find_postorder(self, query_function: Callable[[Node[T]], bool]) -> Node[T] | None:
        for node in self.postorder_traversal(self.root):
            if query_function(node):
                return node
        return None
    
    def _find_levelorder(self, query_function: Callable[[Node[T]], bool]) -> Node[T] | None:
        for node in self.levelorder_traversal(self.root):
            if query_function(node):
                return node
        return None
    
    def _find_upwards(self, query_function: Callable[[Node[T]], bool]) -> Node[T] | None:
        for node in self.upwards_traversal(self.root):
            if query_function(node):
                return node
        return None

    def find_all(self, query_function: Callable[[Node[T]], bool], traversal_type: TraversalType | None = None) -> list[Node[T]]:
        if traversal_type is None:
            traversal_type = self.default_traversal_type

        if traversal_type == TraversalType.PREORDER:
            return self._find_all_preorder(query_function)
        elif traversal_type == TraversalType.POSTORDER:
            return self._find_all_postorder(query_function)
        elif traversal_type == TraversalType.LEVELORDER:
            return self._find_all_levelorder(query_function)
        elif traversal_type == TraversalType.UPWARDS:
            return self._find_all_upwards(query_function)
        
    def _find_all_preorder(self, query_function: Callable[[Node[T]], bool]) -> list[Node[T]]:
        return [node for node in self.preorder_traversal(self.root) if query_function(node)]
    
    def _find_all_postorder(self, query_function: Callable[[Node[T]], bool]) -> list[Node[T]]:
        return [node for node in self.postorder_traversal(self.root) if query_function(node)]
    
    def _find_all_levelorder(self, query_function: Callable[[Node[T]], bool]) -> list[Node[T]]:
        return [node for node in self.levelorder_traversal(self.root) if query_function(node)]
    
    def _find_all_upwards(self, query_function: Callable[[Node[T]], bool]) -> list[Node[T]]:
        return [node for node in self.upwards_traversal(self.root) if query_function(node)]
    
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
        
    def clear(self) -> None:
        self.root.clear()

    def copy(self) -> Self[T]:
        return Tree(self.root.copy())
    
    def is_leaf(self, node: Node[T]) -> bool:
        return node.is_leaf()
    
    def is_root(self, node: Node[T]) -> bool:
        return node.is_root()
    
    def is_branch(self, node: Node[T]) -> bool:
        return node.is_branch()
    
    def get_siblings(self, node: Node[T]) -> list[Node[T]]:
        return node.get_siblings()
    
    def get_children(self, node: Node[T]) -> list[Node[T]]:
        return node.get_children()
    
    def get_parent(self, node: Node[T]) -> Node[T] | None:
        return node.get_parent()
    
    def add_child(self, node: Node[T], parent: Node[T] | None = None, conditional: Callable[[Node[T]], bool] | None = None, traversal_type: TraversalType | None = None) -> None:
        if parent is None and conditional is None:
            parent = self.root

        if parent is not None:
            parent.add_child(node)
            return

        if traversal_type is None:
            traversal_type = self.default_traversal_type

        parent = self.find(conditional, traversal_type)

        if parent is not None:
            parent.add_child(node)
            return 
        
        raise ValueError(f"Could not find a parent that satisfies the given condition.")

    def remove_child(self, node: Node[T], parent: Node[T] | None = None, conditional: Callable[[Node[T]], bool] | None = None, traversal_type: TraversalType | None = None) -> None:
        if parent is None and conditional is None:
            parent = self.root

        if parent is not None:
            parent.remove_child(node)
            return

        if traversal_type is None:
            traversal_type = self.default_traversal_type

        parent = self.find(conditional, traversal_type)

        if parent is not None:
            parent.remove_child(node)
            return 
        
        raise ValueError(f"Could not find a parent that satisfies the given condition.")
    
    def add_children(self, nodes: list[Node[T]], parent: Node[T] | None = None, conditional: Callable[[Node[T]], bool] | None = None, traversal_type: TraversalType | None = None) -> None:
        for node in nodes:
            self.add_child(node, parent, conditional, traversal_type)

    def remove_children(self, nodes: list[Node[T]], parent: Node[T] | None = None, conditional: Callable[[Node[T]], bool] | None = None, traversal_type: TraversalType | None = None) -> None:
        for node in nodes:
            self.remove_child(node, parent, conditional, traversal_type)