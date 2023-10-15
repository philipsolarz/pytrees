from typing import Any, Self, Generator
from collections import deque

type S[T] = dict[str, Self | T | list[S[T]]]
# type SQ[T] = dict[Self | T, list[S[T]]]
# type C[T] = list[Self] | list[T] | list[S[T]]
type C[T] = list[Self | T | S[T]]
# type C[T] = Self | T | dict[T | list[T]]
type TChild[T] = Self | T | S[T]
type TChildren[T] = list[Self | T | S[T]]
type TNode[T] = Self | T | S[T]
type TParent[T] = Self | T 
type N[T] = Self | T
    
class Node[T]:
    def __init__(self, parent: Self = None, identity: T = None, children: list[N[T]] = [], max_children: int | None = None) -> None:
        self._parent = parent
        self._identity = identity
        self._max_children = max_children
        if self.max_children is not None:
            if len(children) >= self.max_children:
                raise ValueError(f"Number of children ({len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        self._children = children

    @property
    def parent(self) -> Self:
        return self._parent

    @parent.setter
    def parent(self, parent: Self) -> None:
        self._parent = parent

    def has_parent(self) -> bool:
        return self.parent is not None
    
    def is_root(self) -> bool:
        return not self.has_parent()
    
    @property
    def identity(self) -> T:
        return self._identity

    @identity.setter
    def identity(self, identity: T) -> None:
        self._identity = identity

    def is_empty(self) -> bool:
        return self.identity is None
    
    def has_identity(self) -> bool:
        return not self.is_empty()
    
    def is_anonymous(self) -> bool:
        return not self.has_identity()

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
    def children(self) -> list[Self]:
        return self._children
    
    @children.setter
    def children(self, children: C[T]) -> None:
        if self.max_children is not None:
            if len(children) >= self.max_children:
                raise ValueError(f"Number of children ({len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        self._children = children

    def has_children(self) -> bool:
        return len(self.children) != 0

    def is_leaf(self) -> bool:
        return not self.has_children()

    def is_branch(self) -> bool:
        return self.has_children()

    def preorder_traversal(self) -> Generator[Self, None, None]:
        yield self
        for child in self.children:
            yield from child.preorder_traversal()

    def postorder_traversal(self) -> Generator[Self, None, None]:
        for child in self.children:
            yield from child.postorder_traversal()
        yield self

    def levelorder_traversal(self) -> Generator[Self, None, None]:
        queue = deque([self])
        while queue:
            current = queue.popleft()
            yield current
            queue.extend(current.children)

    def _add_child(self, child: Self) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.append(child)

    def _add_child_from_dict(self, child_as_dict: S[T]) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        child = Node[T].from_dict(child_as_dict)
        self.children.append(child)

    def add_child(self, child: TChild[T]) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        if isinstance(child, Node):
            self.children.append(child)
        elif isinstance(child, dict):
            child = Node[T].from_dict(child)
            self.children.append(child)
        else:
            identity = child
            child = Node(parent=self, identity=identity, max_children=self.max_children)
            self.children.append(child)
    


    def add_children(self, children: TChildren[T]) -> None:
        for child in children:
            self.add_child(child)
    """
    def add_node(self, parent: Self | T, node: TNode[T]) -> None:
        if isinstance(parent, Node):
            for current_node in self.levelorder_traversal():
                if current_node == parent:
                    current_node.add_child(node)
                    break
        else:
            for current_node in self.levelorder_traversal():
                if current_node.identity == parent:
                    current_node.add_child(node)
                    break

    def add_child(self, parent: TParent[T] = None, child: TChild[T] = None) -> None:
        if isinstance(parent, Node):
            for current_node in self.levelorder_traversal():
                if current_node == parent:
                    current_node.add_child(child)
                    break


    def remove_child(self, child: Self | T) -> None:
        if isinstance(child, Node) and child in self.children:
            self.children.remove(child)
        else:
            for node in self.children:
                if node.identity == child:
                    self.children.remove(node)
                    break

    def remove_children(self, children: list[Self | T]) -> None:
        for child in children:
            self.remove_child(child)
    """

    
    @classmethod
    def from_dict(cls, node_as_dict: S[T]):
        identity = node_as_dict.get("identity")
        max_children = node_as_dict.get("max_children")
        children_as_dicts = node_as_dict.get("children", [])
        
        children = [cls.from_dict(child_as_dict) for child_as_dict in children_as_dicts if isinstance(child_as_dict, dict)]
        
        return cls(identity=identity, max_children=max_children, children=children)
    
    def to_dict(self) -> S[T]:
        result = {
            "identity": self.identity,
            "children": [child.to_dict() for child in self.children]
        }
        if self.max_children is not None:
            result["max_children"] = self.max_children
        return result



inttree_dict = {
    "identity": 1,
    "children": [
        {
            "identity": 2,
            "children": [
                {
                    "identity": 3,
                    "children": [
                        {
                            "identity": 4,
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
}
print(inttree_dict)
node = Node[int].from_dict(inttree_dict)


# print(node.children)
inttree_dict_2 = node.to_dict()
print("----")
print(inttree_dict_2)


