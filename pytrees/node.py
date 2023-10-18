from typing import Self, Generator, Callable, Any
from collections import deque
from basenode import BaseNode
type S[T] = dict[str, Self | T | list[S[T]]]

class Node[T](BaseNode[T]):
    def __init__(self, parent: Self[T] = None, identity: T = None, children: list[Self[T]] = [], max_children: int | None = None) -> None:
        super().__init__(identity=identity)
        self._parent = parent
        self._max_children = max_children
        if self.max_children is not None:
            if len(children) >= self.max_children:
                raise ValueError(f"Number of children ({len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        self._children = children

    @property
    def parent(self) -> Self[T]:
        return self._parent

    @parent.setter
    def parent(self, parent: Self[T]) -> None:
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
    def children(self) -> list[Self[T]]:
        return self._children
    
    @children.setter
    def children(self, children: Self[T]) -> None:
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

    def add_child(self, child: Self[T]) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.append(child)
        child.parent = self

    def add_children(self, children: list[Self[T]]) -> None:
        if self.max_children is not None:
            if len(self.children) + len(children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children) + len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.extend(children)
        for child in children:
            child.parent = self

    def remove_child(self, child: Self[T]) -> None:
        self.children.remove(child)
        child.parent = None

    def remove_children(self, children: list[Self[T]]) -> None:
        for child in children:
            self.children.remove(child)
            child.parent = None

    def clear_children(self) -> None:
        for child in self.children:
            child.parent = None
        self.children.clear()

    @classmethod
    def _from_dict(cls, node_as_dict: S[T], parent: Self[T] = None):
        identity = node_as_dict.get("identity")
        max_children = node_as_dict.get("max_children")
        children_as_dicts = node_as_dict.get("children", [])
        
        node = cls(parent=parent, identity=identity, max_children=max_children)
        
        children = [cls._from_dict(child_as_dict, node) for child_as_dict in children_as_dicts if isinstance(child_as_dict, dict)]
        node.children = children
        
        return node
    
    @classmethod
    def from_dict(cls, node_as_dict: S[T]):
        parent = node_as_dict.get("parent", None)
        if parent and not isinstance(parent, cls):
            raise ValueError(f"Parent node must be of type {cls.__name__} or None.")
        return cls._from_dict(node_as_dict, parent)

    def to_dict(self) -> S[T]:
        node_as_dict = {}
        if self.has_parent():
            node_as_dict["parent"] = self.parent
        if self.has_identity():
            node_as_dict["identity"] = self.identity
        if self.max_children is not None:
            node_as_dict["max_children"] = self.max_children
        if self.has_children():
            node_as_dict["children"] = [child.to_dict() for child in self.children]
        return node_as_dict

    def preorder_traversal(self, callback: Callable[[Self[T]], bool] | None = None) -> Generator[Self[T], None, None]:
        if callback is not None and not callback(self):
            return
        yield self
        for child in self.children:
            yield from child.preorder_traversal(callback)

    def postorder_traversal(self, callback: Callable[[Self[T]], bool] | None = None) -> Generator[Self[T], None, None]:
        if callback is not None and not callback(self):
            return
        for child in self.children:
            yield from child.postorder_traversal(callback)
        yield self

    def levelorder_traversal(self, callback: Callable[[Self[T]], bool] | None = None) -> Generator[Self[T], None, None]:
        queue = deque([self])
        while queue:
            current = queue.popleft()
            if callback is not None and not callback(current):
                return
            yield current
            queue.extend(current.children)

    def upwards_traversal(self, callback: Callable[[Self[T]], bool] | None = None) -> Generator[Self[T], None, None]:
        current = self
        while current is not None:
            if callback is not None and not callback(current):
                return
            yield current
            current = current.parent

    def is_ancestor_of(self, other: Self[T]) -> bool:
        """Returns True if self is an ancestor of other, False otherwise."""
        for node in other.upwards_traversal():
            if node == self:
                return True
        return False
    
    def is_descendant_of(self, other: Self[T]) -> bool:
        """Returns True if self is a descendant of other, False otherwise."""
        for node in self.upwards_traversal():
            if node == other:
                return True
        return False
    
    def is_sibling_with(self, other: Self[T]) -> bool:
        """Returns True if self is a sibling of other, False otherwise."""
        return self.parent == other.parent
    
    def __lt__(self, other: Self[T]) -> bool:
        # self < other
        return self.is_ancestor_of(other)
    
    def __le__(self, other: Self[T]) -> bool:
        # self <= other
        return self.is_ancestor_of(other) or self.is_sibling_with(other)
    
    def __eq__(self, other: Self[T]) -> bool:
        # self == other
        return self.is_sibling_with(other)
    
    def __ne__(self, other: Self[T]) -> bool:
        # self != other
        return not self.is_sibling_with(other)
    
    def __gt__(self, other: Self[T]) -> bool:
        # self > other
        return self.is_descendant_of(other)
    
    def __ge__(self, other: Self[T]) -> bool:
        # self >= other
        return self.is_descendant_of(other) or self.is_sibling_with(other)
    
    def lowest_common_ancestor(self, other: Self[T]) -> Self[T]:
        ancestors = set(self.upwards_traversal())
        for ancestor in other.upwards_traversal():
            if ancestor in ancestors:
                return ancestor
        raise ValueError(f"Nodes {self} and {other} do not share a common ancestor.")
    
    def get_path(self, other: Self[T]) -> list[Self[T]]:
        path_self_to_root = [node for node in self.upwards_traversal()]
        
        path_other_to_lca = [node for node in other.upwards_traversal(lambda node: node not in path_self_to_root)]
        
        if not path_other_to_lca or path_other_to_lca[-1] not in path_self_to_root:
            return []
        
        lca_index = path_self_to_root.index(path_other_to_lca[-1])
        return path_self_to_root[:lca_index] + path_other_to_lca[::-1]
    
    def get_distance(self, other: Self[T]) -> int:
        path = self.get_path(other)
        return len(path)
    
    def get_siblings(self) -> list[Self[T]]:
        if self.is_root():
            return []
        return [child for child in self.parent.children if child != self]
        
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