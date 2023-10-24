from pytrees.node import Node
from typing import Callable, Generator, Self, Iterable
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

type NNQ[T] = Node[T] | list[Node[T]] | Q[T] | QL[T]

type NestedListOfNodes[T] = list[NestedListOfNodes[Node[T]]] | Node[T]
type Query[T] = Callable[[NestedListOfNodes[T]], bool]
type NestedListOfNodesOrQuery[T] = NestedListOfNodes[T] | Query[T]

type NodeOrListOfNodesOrQuery[T] = Node[T] | list[Node[T]] | Query[T]

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
    


    def lca(self, x: NNQ[T], y: NNQ[T], limit: int | None = None, offset: int | None = None, traversal_type: TT = None, 
            return_type: str = 'scalar', flatten: bool = True) -> Node[T] | list[Node[T]] | list[list[Node[T]]]:
        # Handle case where either x or y is None
        if x is None:
            x = y
        elif y is None:
            y = x

        if x is None and y is None:
            if return_type == 'scalar':
                return None
            return [] if flatten else [[]]
        
        if isinstance(x, Node):
            x = list(x)
        elif isinstance(x, list):
            x = x
        elif callable(x):
            x = self.find_all(x, limit, offset, traversal_type)
        else:
            raise ValueError(f"x must be a Node, a list of Nodes, or a callable query that returns a bool.")
        if isinstance(y, Node):
            y = list(y)
        elif isinstance(y, list):
            y = y
        elif callable(y):
            y = self.find_all(y, limit, offset, traversal_type)
        else:
            raise ValueError(f"y must be a Node, a list of Nodes, or a callable query that returns a bool.")
        
        # If x and y are the same list, we can optimize by exploiting symmetry.
        symmetric = x is y

        matrix = []

        for i, node_x in enumerate(x):
            row = []
            start_j = i + 1 if symmetric else 0
            for j, node_y in enumerate(y[start_j:], start=start_j):
                row.append(node_x.lca(node_y))
            matrix.append(row)

        if return_type == 'matrix':
            if not flatten or symmetric:
                return matrix
            else:
                flattened = [lca_node for row in matrix for lca_node in row]
                return flattened

        # For scalar return type
        lca_list = [lca_node for row in matrix for lca_node in row]

        if not lca_list:
            return None  # Handle empty list case

        final_lca = lca_list[0]
        for node in lca_list[1:]:
            final_lca = final_lca.lca(node)

        return final_lca
    
    def lca2(self, *args: NNQ[T], limit: int | None = None, offset: int | None = None, traversal_type: TT = None, 
            return_type: str = 'scalar', flatten: bool = True) -> Node[T] | list[Node[T]] | list[list[Node[T]]]:

        def flatten_nested_list(nested_list: Iterable) -> list[Node[T]]:
            """Recursively flatten nested lists."""
            flat_list = []
            for item in nested_list:
                if isinstance(item, list):
                    flat_list.extend(flatten_nested_list(item))
                else:
                    flat_list.append(item)
            return flat_list

        nodes = []
        for arg in args:
            if arg is None:
                continue
            elif isinstance(arg, Node):
                nodes.append([arg])
            elif isinstance(arg, list):
                nodes.append(arg)
            elif callable(arg):
                nodes.append(self.find_all(arg, limit, offset, traversal_type))
            else:
                raise ValueError(f"Argument must be a Node, a list of Nodes, or a callable query that returns a bool.")

        # If there's just one list, duplicate it to maintain compatibility
        if len(nodes) == 1:
            nodes.append(nodes[0])

        def compute_lca_matrix(*args) -> Node[T] | list[Node[T]]:
            """Recursive function to compute the LCA matrix."""
            if len(args) == 1:
                return args[0]
            # Optimize for symmetric matrix
            symmetric = args[-2] is args[-1]
            if symmetric:
                return [[node_x.lca(node_y) for j, node_y in enumerate(args[-1]) if j >= i] for i, node_x in enumerate(args[-2])]
            return [[node_x.lca(node_y) for node_y in args[-1]] for node_x in compute_lca_matrix(*args[:-1])]

        matrix = compute_lca_matrix(*nodes)

        if return_type == 'matrix':
            if not flatten:
                return matrix
            else:
                return flatten_nested_list(matrix)

        # For scalar return type
        flattened = flatten_nested_list(matrix)
        if not flattened:
            return None

        final_lca = flattened[0]
        for node in flattened[1:]:
            final_lca = final_lca.lca(node)

        return final_lca

    def lca3(self, *args: NestedListOfNodesOrQuery[T], limit: int | None = None, offset: int | None = None, traversal_type: TT = None, 
            return_type: str = 'scalar', flatten: bool = True) -> NestedListOfNodes[T]:

        def extract_nodes(arg: NestedListOfNodesOrQuery[T]) -> NestedListOfNodes[T]:
            if isinstance(arg, Node):
                return [arg]
            elif isinstance(arg, list):
                return arg
            elif callable(arg):
                return self.find_all(arg, limit, offset, traversal_type)
            raise ValueError(f"Argument must be a Node, a list of Nodes, or a callable query that returns a bool.")
        
        def flatten_list(nested: list(NestedListOfNodes[T])) -> list[Node[T]]:
            flat = []
            for item in nested:
                if isinstance(item, list):
                    flat.extend(flatten_list(item))
                else:
                    flat.append(item)
            return flat
            
        def compute_lca(*node_lists: list[Node[T]]) -> NestedListOfNodes[T]:
            if len(node_lists) == 1:
                return node_lists[0]

            computed = []
            for combination in zip(*node_lists):
                if all(isinstance(item, Node) for item in combination):
                    lca_node = combination[0]
                    for node in combination[1:]:
                        lca_node = lca_node.lca(node)
                    computed.append(lca_node)
                else:
                    computed.append(compute_lca(*combination))
            return computed
        def compute_lca2(node_structure: NestedListOfNodes[T]) -> NestedListOfNodes[T]:
            if isinstance(node_structure, Node):
                return node_structure

            computed = []
            for item in node_structure:
                if isinstance(item, Node):
                    computed.append(item)
                else:
                    # Recursive call
                    computed_item = compute_lca(item)
                    if all(isinstance(sub_item, Node) for sub_item in computed_item):
                        lca_node = computed_item[0]
                        for node in computed_item[1:]:
                            lca_node = lca_node.lca(node)
                        computed.append(lca_node)
                    else:
                        computed.append(computed_item)
            return computed


        nodes = [extract_nodes(arg) for arg in args if arg is not None]
        result = compute_lca(*nodes)

        if return_type == 'matrix':
            return flatten_list(result) if flatten else result

        # For scalar return type
        if isinstance(result, Node):
            return result

        flattened = flatten_list(result)
        scalar_lca = flattened[0]
        for node in flattened[1:]:
            scalar_lca = scalar_lca.lca(node)

        return scalar_lca







    def path(self, x: NNQ[T], y: NNQ[T], limit: int | None = None, offset: int | None = None, traversal_type: TT = None, 
         return_type: str = 'scalar', flatten: bool = True) -> list[Node[T]] | list[list[Node[T]]] | list[list[list[Node[T]]]]:
        # Handle case where either x or y is None
        if x is None:
            x = y
        elif y is None:
            y = x
        
        if x is None and y is None:
            if return_type == 'scalar':
                return None
            return [] if flatten else [[]]
        
        if isinstance(x, Node):
            x = list(x)
        elif isinstance(x, list):
            x = x
        elif callable(x):
            x = self.find_all(x, limit, offset, traversal_type)
        else:
            raise ValueError(f"x must be a Node, a list of Nodes, or a callable query that returns a bool.")
        if isinstance(y, Node):
            y = list(y)
        elif isinstance(y, list):
            y = y
        elif callable(y):
            y = self.find_all(y, limit, offset, traversal_type)
        else:
            raise ValueError(f"y must be a Node, a list of Nodes, or a callable query that returns a bool.")

        # If x and y are the same list, we can optimize by exploiting symmetry.
        symmetric = x is y

        matrix = []

        for i, node_x in enumerate(x):
            row = []
            start_j = i + 1 if symmetric else 0
            for j, node_y in enumerate(y[start_j:], start=start_j):
                row.append(node_x.path(node_y))
            matrix.append(row)

        if return_type == 'matrix':
            if not flatten or symmetric:
                return matrix
            else:
                flattened = [path for row in matrix for path in row]
                return flattened

        # For scalar return type
        # Constructing a path that crosses each node in the matrix at least once is non-trivial
        # One way to do it is to simply concatenate the paths, but it might produce redundant paths
        # We'll use a naive way here and improvements can be made for more optimized paths
        scalar_path = []
        for row in matrix:
            for path in row:
                for node in path:
                    if node not in scalar_path:
                        scalar_path.append(node)

        return scalar_path
    
    def distance(self, x: NNQ[T], y: NNQ[T], limit: int | None = None, offset: int | None = None, traversal_type: TT = None, 
                return_type: str = 'scalar', flatten: bool = True, aggregate: str = 'max') -> float | list[float] | list[list[float]]:
        # Handle case where either x or y is None
        if x is None:
            x = y
        elif y is None:
            y = x

        if x is None and y is None:
            if return_type == 'scalar':
                return None
            return [] if flatten else [[]]
        
        if isinstance(x, Node):
            x = list(x)
        elif isinstance(x, list):
            x = x
        elif callable(x):
            x = self.find_all(x, limit, offset, traversal_type)
        else:
            raise ValueError(f"x must be a Node, a list of Nodes, or a callable query that returns a bool.")
        if isinstance(y, Node):
            y = list(y)
        elif isinstance(y, list):
            y = y
        elif callable(y):
            y = self.find_all(y, limit, offset, traversal_type)
        else:
            raise ValueError(f"y must be a Node, a list of Nodes, or a callable query that returns a bool.")
        symmetric = x is y

        matrix = []

        for i, node_x in enumerate(x):
            row = []
            start_j = i + 1 if symmetric else 0
            for j, node_y in enumerate(y[start_j:], start=start_j):
                row.append(node_x.distance(node_y))
            matrix.append(row)

        if return_type == 'matrix':
            if flatten or symmetric:
                flattened_aggregated = []
                for row in matrix:
                    if aggregate == 'min':
                        flattened_aggregated.append(min(row))
                    elif aggregate == 'avg':
                        flattened_aggregated.append(sum(row) / len(row) if row else 0.0)
                    elif aggregate == 'max':
                        flattened_aggregated.append(max(row))
                    else:
                        raise ValueError(f"Invalid aggregate type: {aggregate}")
                return flattened_aggregated
            else:
                return matrix

        # For scalar return type
        distances = [dist for row in matrix for dist in row]

        if aggregate == 'min':
            return min(distances)
        elif aggregate == 'avg':
            return sum(distances) / len(distances) if distances else 0.0
        elif aggregate == 'max':
            return max(distances)
        else:
            raise ValueError(f"Invalid aggregate type: {aggregate}")


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


    def lowest_common_ancestor(self, node1: NNQ[T], node2: NNQ[T], traversal_type: TT = None) -> Node[T]:
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
        return node1.lca(node2)
    
    def lowest_common_ancestors(self, nodes: NQL[T], traversal_type: TT = None) -> list[list[Node[T]]]:
        if isinstance(nodes, list):
            nodes = nodes
        elif callable(nodes):
            nodes = self.find_all(nodes, traversal_type)
        else:
            raise ValueError(f"nodes must be a list of Nodes, or a callable query that returns a bool.")
        return [[self.lca(node1, node2) for node2 in nodes] for node1 in nodes]
    
    
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
    
    def get_paths(self, nodes: NQL[T], traversal_type: TT = None) -> list[list[Node[T]]]:
        if isinstance(nodes, list):
            nodes = nodes
        elif callable(nodes):
            nodes = self.find_all(nodes, traversal_type)
        else:
            raise ValueError(f"nodes must be a list of Nodes, or a callable query that returns a bool.")
        return [[self.get_path(node1, node2) for node2 in nodes] for node1 in nodes]
        
    
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
    
    def get_distances(self, nodes: NQL[T], traversal_type: TT = None) -> list[list[int]]:
        if isinstance(nodes, list):
            nodes = nodes
        elif callable(nodes):
            nodes = self.find_all(nodes, traversal_type)
        else:
            raise ValueError(f"nodes must be a list of Nodes, or a callable query that returns a bool.")
        return [[self.get_distance(node1, node2) for node2 in nodes] for node1 in nodes]