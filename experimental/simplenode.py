from typing import Self, Generator, Callable, Any
from collections import deque
from rich.tree import Tree
from rich import print
type S[T] = dict[str, Self | T | list[S[T]]]

class Node[T]:
    def __init__(self, parent: Self = None, identity: T = None, children: list[Self] = [], max_children: int | None = None) -> None:
        self._parent = parent
        self._identity = identity
        self._max_children = max_children
        if self.max_children is not None:
            if len(children) >= self.max_children:
                raise ValueError(f"Number of children ({len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        self._children = children

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        return self.identity
    
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

    def preorder_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        if callback is not None and not callback(self):
            return
        yield self
        for child in self.children:
            yield from child.preorder_traversal(callback)

    def postorder_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        if callback is not None and not callback(self):
            return
        for child in self.children:
            yield from child.postorder_traversal(callback)
        yield self

    def levelorder_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        queue = deque([self])
        while queue:
            current = queue.popleft()
            yield current
            queue.extend(current.children)

    def upwards_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        current = self
        while current is not None:
            yield current
            current = current.parent

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
    def _from_dict(cls, node_as_dict: S[T], parent: Self = None):
        identity = node_as_dict.get("identity")
        max_children = node_as_dict.get("max_children")
        children_as_dicts = node_as_dict.get("children", [])
        
        node = cls(identity=identity, max_children=max_children, parent=parent)
        
        children = [cls._from_dict(child_as_dict, node) for child_as_dict in children_as_dicts if isinstance(child_as_dict, dict)]
        node.children = children
        
        return node
    
    @classmethod
    def from_dict(cls, node_as_dict: S[T]):
        return cls._from_dict(node_as_dict)

    
    def to_dict(self) -> S[T]:
        result = {
            "identity": self.identity,
            "children": [child.to_dict() for child in self.children]
        }
        if self.max_children is not None:
            result["max_children"] = self.max_children
        return result
    
    def lowest_common_ancestor(self, other: Self) -> Self:
        ancestors = set(self.upwards_traversal())
        for ancestor in other.upwards_traversal():
            if ancestor in ancestors:
                return ancestor
        raise ValueError(f"Nodes {self} and {other} do not share a common ancestor.")
    
    def get_path(self, other: Self) -> list[Self]:
        ancestor = self.lowest_common_ancestor(other)
        self_path = list(self.upwards_traversal())
        other_path = list(other.upwards_traversal())
        other_path.reverse()
        path = self_path + other_path
        path.remove(ancestor)
        return path
    
    def get_distance(self, other: Self) -> int:
        path = self.get_path(other)
        return len(path)
    
    def get_depth(self) -> int:
        return len(list(self.upwards_traversal()))
    
    def get_height(self) -> int:
        return max([len(list(child.preorder_traversal())) for child in self.children]) if self.has_children() else 0
    
    def get_size(self) -> int:
        return len(list(self.preorder_traversal()))

    def _to_rich_tree(self, parent_tree: Tree) -> None:
        """
        Recursively construct a Rich Tree from the node.
        """
        current_tree = parent_tree.add(f"{self.identity}")
        
        for child in self.children:
            child._to_rich_tree(current_tree)

    def print_subtree(self) -> None:
        """
        Print the subtree using the rich library's Tree component.
        """
        tree = Tree(f"{self.identity}")
        
        for child in self.children:
            child._to_rich_tree(tree)

        print(tree)
        
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