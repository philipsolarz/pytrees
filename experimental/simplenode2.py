from typing import Self, Generator, Callable, Any

from rich import print
from basenode import BaseNode
type S[T] = dict[str, Self | T | list[S[T]]]

class SimpleNode[T](BaseNode[T]):
    def __init__(self, parent: Self = None, identity: T = None, children: list[Self] = [], max_children: int | None = None) -> None:
        super().__init__(identity=identity)
        self._parent = parent
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
    def children(self, children: Self) -> None:
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

    def add_child(self, child: Self) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.append(child)
        child.parent = self

    def add_children(self, children: list[Self]) -> None:
        if self.max_children is not None:
            if len(self.children) + len(children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children) + len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.extend(children)
        for child in children:
            child.parent = self

    def remove_child(self, child: Self) -> None:
        self.children.remove(child)
        child.parent = None

    def remove_children(self, children: list[Self]) -> None:
        for child in children:
            self.children.remove(child)
            child.parent = None

    def clear_children(self) -> None:
        for child in self.children:
            child.parent = None
        self.children.clear()
    
    @classmethod
    def from_dict(cls, node_as_dict: S[T]):
        parent = node_as_dict.get("parent", None)
        if parent and not isinstance(parent, cls):
            raise ValueError(f"Parent node must be of type {cls.__name__} or None.")
        identity = node_as_dict.get("identity", None)
        max_children = node_as_dict.get("max_children", None)
        children = node_as_dict.get("children", [])
        for child in children:
            if child and not isinstance(child, cls):
                raise ValueError(f"Child nodes must be of type {cls.__name__} or None.")
        return cls(identity=identity, max_children=max_children, parent=parent, children=children)

    def to_dict(self) -> S[T]:
        node_as_dict = {}
        if self.has_parent():
            node_as_dict["parent"] = self.parent
        if self.has_identity():
            node_as_dict["identity"] = self.identity
        if self.max_children is not None:
            node_as_dict["max_children"] = self.max_children
        if self.has_children():
            node_as_dict["children"] = [child for child in self.children]
        return node_as_dict
    
 
        
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
                            "children": [
                                {
                                    "identity": 5,
                                    "children": []
                                },
                                {
                                    "identity": 6,
                                    "children": []
                                }
                            ]
                        }
                    ]
                },
                {
                    "identity": 7,
                    "children": [
                        {
                            "identity": 8,
                            "children": []
                        },
                        {
                            "identity": 9,
                            "children": []
                        }
                    ]
                }
            ]
        },
        {
            "identity": 10,
            "children": [
                {
                    "identity": 11,
                    "children": []
                },
                {
                    "identity": 12,
                    "children": []
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


for x in node.preorder_traversal():
    print(f"{x.identity} | {x.parent.identity if x.parent else None}")
print("----")
for x in node.postorder_traversal():
    print(f"{x.identity} | {x.parent.identity if x.parent else None}")
print("----")
for x in node.levelorder_traversal():
    print(f"{x.identity} | {x.parent.identity if x.parent else None}")
    test = x
print("----")
for x in test.upwards_traversal():
    print(f"{x.identity} | {x.parent.identity if x.parent else None}")

node.print_subtree()