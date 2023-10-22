from typing import Self, Generator, Callable, Any
from collections import deque
from pytrees.basenode import BaseNode
from rich.tree import Tree as RichTree
from rich import print
type S[T] = dict[str, Self | T | list[S[T]]]

class Node[T]:
    def __init__(self, source: Self = None, identity: T = None, branches: list[Self] | None = None, max_branches: int | None = None) -> None:
        self._source = source
        self._identity = identity
        if branches is None:
            branches = []
        self._max_branches = max_branches
        if self.max_branches is not None:
            if len(branches) >= self.max_branches:
                raise ValueError(f"Number of branches ({len(branches)}) cannot exceed maximum number of branches ({self.max_branches}).")
        self._branches = branches

    def __call__(self, *args, **kwargs):
        return self.identity
    
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
    def source(self) -> Self:
        return self._source

    @source.setter
    def source(self, source: Self) -> None:
        self._source = source

    def has_source(self) -> bool:
        return self.source is not None
    
    def is_root(self) -> bool:
        return not self.has_source()

    @property
    def max_branches(self) -> int | None:
        return self._max_branches

    @max_branches.setter
    def max_branches(self, max_branches: int | None) -> None:
        if max_branches is not None:
            if max_branches < 0:
                raise ValueError(f"Maximum number of branches ({max_branches}) must be a positive integer.")
        if len(self.branches) > max_branches:
            raise ValueError(f"The maximum number of branches ({max_branches}) cannot be less than the current number of branches ({len(self.branches)}).")
        self._max_branches = max_branches

    @property
    def branches(self) -> list[Self]:
        return self._branches
    
    @branches.setter
    def branches(self, branches: Self) -> None:
        if self.max_branches is not None:
            if len(branches) >= self.max_branches:
                raise ValueError(f"Number of branches ({len(branches)}) cannot exceed maximum number of branches ({self.max_branches}).")
        self._branches = branches

    def has_branches(self) -> bool:
        return len(self.branches) != 0

    def is_sink(self) -> bool:
        return not self.has_branches()

    def add_branch(self, branch: Self) -> None:
        
        if self.max_branches is not None:
            if len(self.branches) >= self.max_branches:
                raise ValueError(f"Number of branches ({len(self.branches)}) cannot exceed maximum number of branches ({self.max_branches}).")
        self.branches.append(branch)
        branch.source = self
        


    def add_branches(self, branches: list[Self]) -> None:
        if self.max_branches is not None:
            if len(self.branches) + len(branches) >= self.max_branches:
                raise ValueError(f"Number of branches ({len(self.branches) + len(branches)}) cannot exceed maximum number of branches ({self.max_branches}).")
        self.branches.extend(branches)
        for branch in branches:
            branch.source = self

    def remove_branch(self, branch: Self) -> None:
        self.branches.remove(branch)
        branch.source = None

    def remove_branches(self, branches: list[Self]) -> None:
        for branch in branches:
            self.branches.remove(branch)
            branch.source = None

    def clear_branches(self) -> None:
        for branch in self.branches:
            branch.source = None
        self.branches.clear()

    @classmethod
    def _from_dict(cls, node_as_dict: S[T], source: Self = None):
        identity = node_as_dict.get("identity")
        max_branches = node_as_dict.get("max_branches")
        branches_as_dicts = node_as_dict.get("branches", [])
        
        node = cls(source=source, identity=identity, max_branches=max_branches)
        
        branches = [cls._from_dict(branch_as_dict, node) for branch_as_dict in branches_as_dicts if isinstance(branch_as_dict, dict)]
        node.branches = branches
        
        return node
    
    @classmethod
    def from_dict(cls, node_as_dict: S[T]):
        source = node_as_dict.get("source", None)
        if source and not isinstance(source, cls):
            raise ValueError(f"Source node must be of type {cls.__name__} or None.")
        return cls._from_dict(node_as_dict, source)

    def to_dict(self) -> S[T]:
        node_as_dict = {}
        if self.has_source():
            node_as_dict["source"] = self.source
        if self.has_identity():
            node_as_dict["identity"] = self.identity
        if self.max_branches is not None:
            node_as_dict["max_branches"] = self.max_branches
        if self.has_branches():
            node_as_dict["branches"] = [branch.to_dict() for branch in self.branches]
        return node_as_dict

    def preorder_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        if callback is not None and not callback(self):
            return
        yield self
        for branch in self.branches:
            yield from branch.preorder_traversal(callback)

    def postorder_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        if callback is not None and not callback(self):
            return
        for branch in self.branches:
            yield from branch.postorder_traversal(callback)
        yield self

    def levelorder_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        queue = deque([self])
        while queue:
            current = queue.popleft()
            if callback is not None and not callback(current):
                return
            yield current
            queue.extend(current.branches)

    def upwards_traversal(self, callback: Callable[[Self], bool] | None = None) -> Generator[Self, None, None]:
        current = self
        while current is not None:
            if callback is not None and not callback(current):
                return
            yield current
            current = current.source

    def is_ancestor_of(self, other: Self) -> bool:
        """Returns True if self is an ancestor of other, False otherwise."""
        for node in other.upwards_traversal():
            if node == self:
                return True
        return False
    
    def is_descendant_of(self, other: Self) -> bool:
        """Returns True if self is a descendant of other, False otherwise."""
        for node in self.upwards_traversal():
            if node == other:
                return True
        return False
    
    def is_sibling_with(self, other: Self) -> bool:
        """Returns True if self is a sibling of other, False otherwise."""
        return self.source == other.source
    
    def __lt__(self, other: Self) -> bool:
        # self < other
        return self.is_ancestor_of(other)
    
    def __le__(self, other: Self) -> bool:
        # self <= other
        return self.is_ancestor_of(other) or self.is_sibling_with(other)
    
    def __eq__(self, other: Self) -> bool:
        # self == other
        return self.is_sibling_with(other)
    
    def __ne__(self, other: Self) -> bool:
        # self != other
        return not self.is_sibling_with(other)
    
    def __gt__(self, other: Self) -> bool:
        # self > other
        return self.is_descendant_of(other)
    
    def __ge__(self, other: Self) -> bool:
        # self >= other
        return self.is_descendant_of(other) or self.is_sibling_with(other)
    
    def lowest_common_ancestor(self, other: Self) -> Self:
        ancestors = set(self.upwards_traversal())
        for ancestor in other.upwards_traversal():
            if ancestor in ancestors:
                return ancestor
        raise ValueError(f"Nodes {self} and {other} do not share a common ancestor.")
    
    def get_path(self, other: Self) -> list[Self]:
        path_self_to_root = [node for node in self.upwards_traversal()]
        
        path_other_to_lca = [node for node in other.upwards_traversal(lambda node: node not in path_self_to_root)]
        
        if not path_other_to_lca or path_other_to_lca[-1] not in path_self_to_root:
            return []
        
        lca_index = path_self_to_root.index(path_other_to_lca[-1])
        return path_self_to_root[:lca_index] + path_other_to_lca[::-1]
    
    def get_distance(self, other: Self) -> int:
        path = self.get_path(other)
        return len(path)
    
    def get_siblings(self) -> list[Self]:
        if self.is_root():
            return []
        return [branch for branch in self.source.branches if branch != self]
    
    def display_tree(self):
        """Displays the tree using the Rich library."""

        def build_rich_tree(node, parent_rich_tree=None):
            """Recursively build a RichTree from the given node."""
            if parent_rich_tree is None:
                rich_tree = RichTree(f"{node.identity}")
            else:
                rich_tree = parent_rich_tree.add(f"{node.identity}")
            for branch in node.branches:
                build_rich_tree(branch, rich_tree)
            
            return rich_tree
        
        tree = build_rich_tree(self)
        print(tree)

if __name__ == "__main__":
    inttree_dict = {
        "identity": 1,
        "branches": [
            {
                "identity": 2,
                "branches": [
                    {
                        "identity": 3,
                        "branches": [
                            {
                                "identity": 4,
                                "branches": [
                                    {
                                        "identity": 5,
                                        "branches": []
                                    },
                                    {
                                        "identity": 6,
                                        "branches": []
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "identity": 7,
                        "branches": [
                            {
                                "identity": 8,
                                "branches": []
                            },
                            {
                                "identity": 9,
                                "branches": []
                            }
                        ]
                    }
                ]
            },
            {
                "identity": 10,
                "branches": [
                    {
                        "identity": 11,
                        "branches": []
                    },
                    {
                        "identity": 12,
                        "branches": []
                    }
                ]
            }
        ]
    }

    print(inttree_dict)
    node = Node[int].from_dict(inttree_dict)


    # print(node.branches)
    inttree_dict_2 = node.to_dict()
    print("----")
    print(inttree_dict_2)


    for x in node.preorder_traversal():
        print(f"{x.identity} | {x.source.identity if x.source else None}")
    print("----")
    for x in node.postorder_traversal():
        print(f"{x.identity} | {x.source.identity if x.source else None}")
    print("----")
    for x in node.levelorder_traversal():
        print(f"{x.identity} | {x.source.identity if x.source else None}")
        test = x
    print("----")
    for x in test.upwards_traversal():
        print(f"{x.identity} | {x.source.identity if x.source else None}")

    node.print_subtree()