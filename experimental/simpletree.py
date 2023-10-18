from experimental.simplenode2 import SimpleNode as Node

from collections import deque
from rich.tree import Tree

# type N[T] = Node[T] 

class Tree[T]:
    def __init__(self, root: Node[T], max_children: int | None = None) -> None:
        if max_children is not None:
                if len(root.children) > max_children:
                    raise ValueError(f"Node cannot have more than {max_children} children.")
        self._root = root
        self._max_children = max_children
        

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