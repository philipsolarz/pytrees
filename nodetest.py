from typing import Any, Self, Generator
from collections import deque

type S[T] = dict[str, Self | T | list[S[T]]]
type SQ[T] = dict[Self | T, list[S[T]]]
# type C[T] = list[Self] | list[T] | list[S[T]]
type C[T] = list[Self | T | S[T]]
# type C[T] = Self | T | dict[T | list[T]]
type TChild[T] = Self | T | S[T]
type TChildren[T] = list[Self | T | S[T]]
type TNode[T] = Self | T | S[T]
type TParent[T] = Self | T 

class BaseNode[T]:
    def __init__(self, parent: Self = None, identity: T = None, children: C[T] = [], max_children: int | None = None) -> None:
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
    
class Node[T](BaseNode[T]):
    def __init__(self, parent: Self = None, identity: T = None, children: C[T] = [], max_children: int | None = None) -> None:
        super().__init__(parent=parent, identity=identity, children=children, max_children=max_children)

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

    def add_child(self, child: TChild[T], validate_subtree: bool = True) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        if isinstance(child, Node):
            self.children.append(child)
        elif isinstance(child, dict):
            identity = child.get("identity")
            max_children = child.get("max_children", self.max_children)
            grandchildren = child.get("children", [])
            child = Node(parent=self, identity=identity, max_children=max_children, children=grandchildren)
            if not validate_subtree:
                self.children.append(child)
            for grandchild in grandchildren:
                child.add_child(grandchild)
            if validate_subtree:
                self.children.append(child)
        else:
            identity = child
            child = Node(parent=self, identity=identity, max_children=self.max_children)
            self.children.append(child)
    
    def add_children(self, children: TChildren[T]) -> None:
        for child in children:
            self.add_child(child)

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

    @classmethod
    def from_dict(cls, node_as_dict: S[T]):
        identity = node_as_dict.get("identity")
        max_children = node_as_dict.get("max_children")
        children_as_dicts = node_as_dict.get("children", [])
        
        node = cls(identity=identity, max_children=max_children)

        for child_as_dict in children_as_dicts:
            if isinstance(child, dict):
                child = cls.from_dict(child_as_dict)
                node.add_child(child)

        return node
    
    def to_dict


# Example usage
def f1():
    pass
def f2():
    pass
def f3():
    pass
def f4():
    pass

functree_dict = {
    "identity": f1,
    "children": [
        {
            "identity": f2,
            "children": [
                {
                    "identity": f3,
                    "children": [
                        {
                            "identity": f4,
                            "children": []
                        }
                    ]
                }
            ]
        }
    ]
}

node = Node.from_dict(functree_dict)

subtree_dict = {
    "identity": "B",
    "children": [
        {
            "identity": "D",
            "children": []
        },
        {
            "identity": "E",
            "children": [
                {
                    "identity": "G",
                    "children": []
                }
            ]
        }
    ]
}

root = Node[str](identity='Root', children=[subtree_dict])
root.build_subtree_from_dict({})
print(root)