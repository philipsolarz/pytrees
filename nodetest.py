from typing import Any, Self
type S[T] = dict[str, Self | T | list[S[T]]]
type SQ[T] = dict[Self | T, list[S[T]]]
# type C[T] = list[Self] | list[T] | list[S[T]]
type C[T] = list[Self | T | S[T]]
# type C[T] = Self | T | dict[T | list[T]]


class Node[T]:
    def __init__(self, parent: Self = None, identity: T = None, children: C[T] = [], max_children: int | None = None) -> None:
        self._parent = parent
        self._identity = identity
        self._max_children = max_children
        self._children = []
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

    @property
    def identity(self) -> T:
        return self._identity

    @identity.setter
    def identity(self, identity: T) -> None:
        self._identity = identity

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

    def add_child(self, child: Self) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.append(child)

    def add_children(self, children: C[T]) -> None:
        for child in children:
            if isinstance(child, Node):
                self.add_child(child)
                child.parent = self
            elif isinstance(child, dict):
                self.add_subtree_from_dict(child)
            else:
                self.add_child(Node(self, child, max_children=self.max_children))

    def add_subtree_from_dict(self, subtree: S[T]) -> None:
        if "identity" not in subtree:
            raise ValueError(f"Node must have an identity.")
        child = Node(parent=self, identity=subtree["identity"], max_children=self.max_children)
        if "children" in subtree:
            children = subtree["children"]
            child.add_children(children)
        self.add_child(child)

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