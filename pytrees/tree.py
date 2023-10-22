from pytrees.node import Node
from typing import Callable, Generator, Self
from collections import deque
from enum import Enum
from rich.tree import Tree as RichTree
class TraversalType(Enum):
    PREORDER = "preorder"
    POSTORDER = "postorder"
    LEVELORDER = "levelorder"
    UPWARDS = "upwards"
    AUTO = "auto"

type S[T] = dict[str, Node[T] | T | list[S[T]]]
type N[T] = Node[T] | T
type Q[T] = Callable[[Node[T]], bool]
type QL[T] = Callable[[list[Node[T]]], bool]
type NQ[T] = Node[T] | Q[T]
type NQL[T] = list[Node[T]] | QL[T]
type NQ_Experimental[T] = Node[T] | Callable[[NQ_Experimental[T]], bool]
type TT = TraversalType | None
type NGen[T] = Generator[Node[T], None, None]

class Tree[T]:
    def __init__(self, root: N[T]) -> None:
        if isinstance(root, Node):
            self._root = root
        else:
            self._root = Node[T](identity=root)
        self._max_branches = self._root.max_branches
        if self._max_branches is not None:
                if len(self._root.branches) > self._max_branches:
                    raise ValueError(f"Node cannot have more than {self._max_branches} branches.")
        self._default_traversal_type = TraversalType.PREORDER
                
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return self.contains_subtree(other) and other.contains_subtree(self)

    def __lt__(self, other: Self) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return other.contains_subtree(self) and not self.__eq__(other)

    def __le__(self, other: Self) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return other.contains_subtree(self)

    def __gt__(self, other: Self) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return self.contains_subtree(other) and not self.__eq__(other)

    def __ge__(self, other: Self) -> bool:
        if not isinstance(other, Tree):
            return NotImplemented
        return self.contains_subtree(other)

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)
    
    @property
    def root(self) -> Node[T]:
        return self._root
    
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
    def default_traversal_type(self) -> TraversalType:
        return self._default_traversal_type
    
    @default_traversal_type.setter
    def default_traversal_type(self, traversal_type: TraversalType) -> None:
        self._default_traversal_type = traversal_type

    @classmethod
    def from_dict(cls, tree_as_dict: dict) -> Self:
        root = Node.from_dict(tree_as_dict)
        return cls(root)
    
    def to_dict(self) -> dict:
        return self.root.to_dict()

    def preorder_traversal(self, node: Node[T], callback: Q[T] | None = None) -> NGen[T]:
        if callback is not None and callback(node):
            return
        yield node
        for branch in node.branches:
            yield from branch.preorder_traversal(callback)

    def postorder_traversal(self, node: Node[T], callback: Q[T] | None = None) -> NGen[T]:
        if callback is not None and callback(node):
            return
        for branch in node.branches:
            yield from branch.postorder_traversal(callback)
        yield node

    def levelorder_traversal(self, node: Node[T], callback: Q[T] | None = None) -> NGen[T]:
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if callback is not None and callback(current):
                return
            yield current
            queue.extend(current.branches)

    def upwards_traversal(self, node: Node[T], callback: Q[T] | None = None) -> NGen[T]:
        current = node
        while current is not None:
            if callback is not None and callback(current):
                return
            yield current
            current = current.source

    def size(self) -> int:
        return len(list(self.levelorder_traversal(self.root)))
    
    def depth(self, node: NQ[T], traversal_type: TT) -> int:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return len(list(self.upwards_traversal(node))) - 1
    
    def depths(self, nodes: NQL[T], limit: int | None, offset: int | None, traversal_type: TT) -> list[int]:
        depths = []
        if isinstance(nodes, list):
            for node in nodes:
                depth = self.depth(node)
                depths.append(depth)
        elif callable(nodes):
            nodes = self.find_all(nodes, limit, offset, traversal_type)
            for node in nodes:
                depth = self.depth(node)
                depths.append(depth)
        else:
            raise ValueError(f"node must be a list of Nodes, or a callable query that returns a bool.")
        return depths
    
    def find(self, query: Q[T], traversal_type: TT = None) -> Node[T] | None:
        if traversal_type is None:
            traversal_type = self.default_traversal_type

        if traversal_type == TraversalType.PREORDER:
            return self._find_preorder(query)
        elif traversal_type == TraversalType.POSTORDER:
            return self._find_postorder(query)
        elif traversal_type == TraversalType.LEVELORDER:
            return self._find_levelorder(query)
        elif traversal_type == TraversalType.UPWARDS:
            return self._find_upwards(query)
        
    def _find_preorder(self, query: Q[T]) -> Node[T] | None:
        for node in self.preorder_traversal(self.root):
            if query(node):
                return node
        return None
    
    def _find_postorder(self, query: Q[T]) -> Node[T] | None:
        for node in self.postorder_traversal(self.root):
            if query(node):
                return node
        return None
    
    def _find_levelorder(self, query: Q[T]) -> Node[T] | None:
        for node in self.levelorder_traversal(self.root):
            if query(node):
                return node
        return None
    
    def _find_upwards(self, query: Q[T]) -> Node[T] | None:
        for node in self.upwards_traversal(self.root):
            if query(node):
                return node
        return None

    def find_all(self, query: Q[T], limit: int | None, offset: int | None, traversal_type: TT = None) -> list[Node[T]]:
        if traversal_type is None:
            traversal_type = self.default_traversal_type

        if traversal_type == TraversalType.PREORDER:
            return self._find_all_preorder(query, limit, offset)
        elif traversal_type == TraversalType.POSTORDER:
            return self._find_all_postorder(query, limit, offset)
        elif traversal_type == TraversalType.LEVELORDER:
            return self._find_all_levelorder(query, limit, offset)
        elif traversal_type == TraversalType.UPWARDS:
            return self._find_all_upwards(query, limit, offset)
        
    def _find_all_preorder(self, query: Q[T], limit: int | None, offset: int | None) -> list[Node[T]]:
        nodes = []
        for node in self.preorder_traversal(self.root):
            if query(node):
                if offset and offset > 0:
                    offset -= 1
                    continue
                nodes.append(node)
                if limit and len(nodes) >= limit:
                    return nodes
        return nodes
        # return [node for node in self.preorder_traversal(self.root) if query(node)]
    
    def _find_all_postorder(self, query: Q[T], limit: int | None, offset: int | None) -> list[Node[T]]:
        nodes = []
        for node in self.postorder_traversal(self.root):
            if query(node):
                if offset and offset > 0:
                    offset -= 1
                    continue
                nodes.append(node)
                if limit and len(nodes) >= limit:
                    return nodes
        return nodes
        # return [node for node in self.postorder_traversal(self.root) if query(node)]
    
    def _find_all_levelorder(self, query: Q[T], limit: int | None, offset: int | None) -> list[Node[T]]:
        nodes = []
        for node in self.levelorder_traversal(self.root):
            if query(node):
                if offset and offset > 0:
                    offset -= 1
                    continue
                nodes.append(node)
                if limit and len(nodes) >= limit:
                    return nodes
        return nodes
        # return [node for node in self.levelorder_traversal(self.root) if query(node)]
    
    def _find_all_upwards(self, query: Q[T], limit: int | None, offset: int | None) -> list[Node[T]]:
        nodes = []
        for node in self.upwards_traversal(self.root):
            if query(node):
                if offset and offset > 0:
                    offset -= 1
                    continue
                nodes.append(node)
                if limit and len(nodes) >= limit:
                    return nodes
        return nodes
        # return [node for node in self.upwards_traversal(self.root) if query(node)]
    
    def lowest_common_ancestor(self, node1: NQ[T], node2: NQ[T], traversal_type: TT = None) -> Node[T]:
        if isinstance(node1, Node):
            node1 = node1
        elif callable(node1):
            node1 = self.find(node1, traversal_type)
        else:
            raise ValueError(f"node1 must be a Node or a callable query that returns a bool.")
        if isinstance(node2, Node):
            node2 = node2
        elif callable(node2):
            node2 = self.find(node2, traversal_type)
        else:
            raise ValueError(f"node2 must be a Node or a callable query that returns a bool.")
        return node1.lowest_common_ancestor(node2)
    
    def lowest_common_ancestors(self, nodes: NQL[T], traversal_type: TT = None) -> list[Node[T]]:
        # Check lowest_common_ancestors between each node in nodes return matrix?
        pass
    
    def get_path(self, node1: NQ[T], node2: NQ[T], traversal_type: TT = None) -> list[Node[T]]:
        if isinstance(node1, Node):
            node1 = node1
        elif callable(node1):
            node1 = self.find(node1, traversal_type)
        else:
            raise ValueError(f"node1 must be a Node or a callable query that returns a bool.")
        if isinstance(node2, Node):
            node2 = node2
        elif callable(node2):
            node2 = self.find(node2, traversal_type)
        else:
            raise ValueError(f"node2 must be a Node or a callable query that returns a bool.")
        return node1.get_path(node2)
    
    def get_distance(self, node1: NQ[T], node2: NQ[T], traversal_type: TT = None) -> int:
        if isinstance(node1, Node):
            node1 = node1
        elif callable(node1):
            node1 = self.find(node1, traversal_type)
        else:
            raise ValueError(f"node1 must be a Node or a callable query that returns a bool.")
        if isinstance(node2, Node):
            node2 = node2
        elif callable(node2):
            node2 = self.find(node2, traversal_type)
        else:
            raise ValueError(f"node2 must be a Node or a callable query that returns a bool.")
        return node1.get_distance(node2)

    def get_subtree(self, node: NQ[T], traversal_type: TT = None) -> Self:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
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

    def copy(self) -> Self:
        return Tree(self.root.copy())
    
    def is_sink(self, node: NQ[T], traversal_type: TT = None) -> bool:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return node.is_sink()
    
    def is_root(self, node: NQ[T], traversal_type: TT = None) -> bool:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return node.is_root()
    
    def is_branch(self, node: NQ[T], traversal_type: TT = None) -> bool:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return node.is_branch()
    
    def get_siblings(self, node: NQ[T], traversal_type: TT = None) -> list[Node[T]]:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return node.get_siblings()
    
    def get_branches(self, node: NQ[T], traversal_type: TT = None) -> list[Node[T]]:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return node.get_branches()
    
    def get_source(self, node: NQ[T], traversal_type: TT = None) -> Node[T] | None:
        if isinstance(node, Node):
            node = node
        elif callable(node):
            node = self.find(node, traversal_type)
        else:
            raise ValueError(f"node must be a Node or a callable query that returns a bool.")
        return node.get_source()
    
    def add_branch(self, node: Node[T] | T, source: NQ[T] | None = None, traversal_type: TT = None) -> Node[T]:
        if isinstance(source, Node):
            source = source
        elif callable(source):
            source = self.find(source, traversal_type)
        else:
            source = self.root

        if isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        if source is not None:
            source.add_branch(node)
            return node
        
        raise ValueError(f"Could not find a source that satisfies the given condition.")

    def remove_branch(self, node: Node[T], source: NQ[T] | None = None, traversal_type: TT = None) -> None:
        if isinstance(source, Node):
            source = source
        elif callable(source):
            source = self.find(source, traversal_type)
        else:
            source = self.root

        if source is not None:
            source.remove_branch(node)
            return
        # Maybe add query possibility to node as well?
        raise ValueError(f"Could not find a source that satisfies the given condition.")
    
    def add_branches(self, nodes: list[Node[T]], source: NQ[T] | None = None, traversal_type: TT = None) -> None:
        for node in nodes:
            return [node for node in self.add_branch(node, source, traversal_type)]
            # self.add_branch(node, source, traversal_type)

    def remove_branches(self, nodes: list[Node[T]], source: NQ[T] | None = None, traversal_type: TT = None) -> None:
        for node in nodes:
            self.remove_branch(node, source, traversal_type)

    def print(self) -> None:
        self.root.print()