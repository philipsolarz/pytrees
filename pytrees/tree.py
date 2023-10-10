from pytrees.node import Node

type N[T] = Node[T] | T | dict[T | list[T]] | None

class Tree[T]:
    """
    A tree is a data structure composed of nodes. 
    Each tree has a root node and zero or more child nodes. 
    Each child node has zero or more child nodes, and so on. A tree cannot contain cycles. 
    The root node has no parent. 
    Every other node has exactly one parent. 
    Each node can have an arbitrary number of children.

    Args:
        T (type): The type of the identity of the nodes in the tree.

    Examples:
    
            >>> tree = Tree()
            >>> tree = Tree(1)
            >>> tree = Tree(Node(1))
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
    """
    def __init__(self, root: N[T] = None, max_children: int | None = None):
        """
        Creates a new tree with the given root node.

        Args:
            root (N[T], optional): The root node of the tree. Defaults to None.
            max_children (int, optional): The maximum number of children each node can have. Defaults to None.

        Raises:
            TypeError: If the root node is not of type Node.

        Examples:

            >>> tree = Tree()
            >>> tree = Tree(1)
            >>> tree = Tree(Node(1))
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
        """
        self.max_children = max_children
        if root is None:
            self.root = None
        elif isinstance(root, Node):
            if self.max_children is not None:
                if len(root.get_children()) > self.max_children:
                    raise ValueError(f"Node cannot have more than {self.max_children} children.")
            self.root = root
        elif isinstance(root, dict):
            if len(root) != 1:
                raise ValueError("There can only be one root node.")
            self.root = Node[T](identity=root.keys()[0], max_children=self.max_children)
            for child in root.values()[0]:
                self.root.add_child(Node[T](identity=child, max_children=self.max_children))


        else:
            self.root = Node[T](identity=root, max_children=self.max_children)

    def is_empty(self) -> bool:
        """
        Returns True if the tree is empty, False otherwise.
        
        Returns:
            bool: True if the tree is empty, False otherwise.
        
        Examples:
        
            >>> tree = Tree()
            >>> tree.is_empty()
            True
            >>> tree = Tree(1)
            >>> tree.is_empty()
            False
            >>> tree = Tree(Node(1))
            >>> tree.is_empty()
            False
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
            >>> tree.is_empty()
            False
        """
        return self.root is None
    
    def get_root(self):
        """
        Returns the root node of the tree.
        
        Returns:
            Node: The root node of the tree.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.get_root()
            None
            >>> tree = Tree(1)
            >>> tree.get_root()
            1
            >>> tree = Tree(Node(1))
            >>> tree.get_root()
            Node(1)
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
            >>> tree.get_root()
            Node(1)
        """
        return self.root
    
    def set_root(self, node: N[T]):
        """
        Sets the root node of the tree.

        Args:
            node (N[T]): The node to set as the root node of the tree.

        Raises:
            TypeError: If the node is not of type Node.

        Examples:
            
                >>> tree = Tree()
                >>> tree.set_root(1)
                >>> tree.get_root()
                1
                >>> tree.set_root(Node(1))
                >>> tree.get_root()
                Node(1)
                >>> tree.set_root(Node(1, [Node(2), Node(3)]))
                >>> tree.get_root()
                Node(1)
        """
        if node is None:
            self.root = None
        elif isinstance(node, Node):
            if self.max_children is not None:
                if len(node.get_children()) > self.max_children:
                    raise ValueError(f"Node cannot have more than {self.max_children} children.")
        else:
            self.root = Node[T](identity=node)

    def get_size(self) -> int:
        """
        Returns the number of nodes in the tree.

        Returns:
            int: The number of nodes in the tree.

        Examples:
            
                >>> tree = Tree()
                >>> tree.get_size()
                0
                >>> tree = Tree(1)
                >>> tree.get_size()
                1
                >>> tree = Tree(Node(1))
                >>> tree.get_size()
                1
                >>> tree = Tree(Node(1, [Node(2), Node(3)]))
                >>> tree.get_size()
                3
        """
        return self.root.get_size()
    
    def get_height(self, node: N[T] = None) -> int:
        """
        Returns the height of the tree.

        Args:
            node (N[T], optional): The node to start the height calculation from. Defaults to None.

        Returns:
            int: The height of the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.get_height()
            0
            >>> tree = Tree(1)
            >>> tree.get_height()
            0
            >>> tree = Tree(Node(1))
            >>> tree.get_height()
            0
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
            >>> tree.get_height()
            1
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        if node.is_leaf():
            return 0
        
        return 1 + max(self.get_height(child) for child in node.get_children())


    def get_depth(self, node: N[T] = None) -> int:
        """
        Returns the depth of the tree.

        Args:
            node (N[T], optional): The node to start the depth calculation from. Defaults to None.

        Returns:
            int: The depth of the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.get_depth()
            0
            >>> tree = Tree(1)
            >>> tree.get_depth()
            0
            >>> tree = Tree(Node(1))
            >>> tree.get_depth()
            0
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
            >>> tree.get_depth()
            0
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
            >>> tree.get_depth(node=2)
            1
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        if node.is_root():
            return 0
        
        return 1 + self.get_depth(node.get_parent())

    def get_parent(self, node: N[T], return_as_node: bool = False) -> N[T]:
        """
        Returns the parent of the given node.
        
        Args:
            node (N[T]): The node whose parent is to be returned.
            return_as_node (bool, optional): If True, the parent node is returned. If False, the identity of the parent node is returned. Defaults to False.

            
        Returns:
            N[T]: The parent of the given node.
            
        Examples:
        
            >>> tree = Tree()
        """
        if node is None:
            return None
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
            
        parent = node.get_parent()

        if return_as_node:
            return parent
        else:
            return parent.get_identity()


    
    def get_children(self, node: N[T], return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the children of the given node.

        Args:
            node (N[T]): The node whose children are to be returned.
            return_as_node (bool, optional): If True, the children nodes are returned. If False, the identities of the children nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The children of the given node.

        Examples:

            >>> tree = Tree()
            >>> tree.get_children(1)
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        children = node.get_children()

        if return_as_node:
            return children
        else:
            return [child.get_identity() for child in children]
    
    def add_child(self, node: N[T], child: N[T]):
        """
        Adds a child to the given node.
        
        Args:
            node (N[T]): The node to add the child to.
            child (N[T]): The child to add to the node.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.add_child(1, 2)
            >>> tree.get_children(1)
            [2]
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        if child is None:
            child = None
        elif isinstance(child, Node):
            child = child
        else:
            child = Node[T](identity=child)

        node.add_child(child)


    def remove_child(self, node: N[T], child: N[T]):
        """
        Removes a child from the given node.

        Args:
            node (N[T]): The node to remove the child from.
            child (N[T]): The child to remove from the node.

        Examples:

            >>> tree = Tree()
            >>> tree.add_child(1, 2)
            >>> tree.get_children(1)
            [2]
            >>> tree.remove_child(1, 2)
            >>> tree.get_children(1)
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        if child is None:
            child = None
        elif isinstance(child, Node):
            child = child
        else:
            child = Node[T](identity=child)
        
        node.remove_child(child)

    def insert_node(self, node: N[T], parent: N[T]):
        """
        Inserts a node into the tree.

        Args:
            node (N[T]): The node to insert.
            parent (N[T] | Callable): The parent of the node to insert.

        Examples:

            >>> tree = Tree()
            >>> tree.insert_node(1, 2)
            >>> tree.get_children(2)
            [1]
        """
        if node is None:
            node = None
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        if parent is None:
            parent = self.root
        elif isinstance(parent, Node):
            parent = parent
        else:
            parent = Node[T](identity=parent)
        
        parent.add_child(node)

    def remove_node(self, node: N[T]):
        """
        Removes a node from the tree.

        Args:
            node (N[T]): The node to remove.

        Examples:
            
                >>> tree = Tree()
                >>> tree.insert_node(1, 2)
                >>> tree.get_children(2)
                [1]
                >>> tree.remove_node(1)
                >>> tree.get_children(2)
                []
            """
        if node is None:
            node = None
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        node.remove()

    def is_leaf(self, node: N[T]) -> bool:
        """
        Returns True if the given node is a leaf, False otherwise.
        
        Args:
            node (N[T]): The node to check.
            
        Returns:
            bool: True if the given node is a leaf, False otherwise.
            
        Examples:
        
            >>> tree = Tree()
            >>> 
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        return node.is_leaf()
    
    def is_root(self, node: N[T]) -> bool:
        """
        Returns True if the given node is the root, False otherwise.
        
        Args:
            node (N[T]): The node to check.
            
        Returns:
            bool: True if the given node is the root, False otherwise.
            
        Examples:
        
            >>> tree = Tree()
            >>>
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        return node.is_root()
    
    def is_internal(self, node: N[T]) -> bool:
        """
        Returns True if the given node is internal, False otherwise.

        Args:
            node (N[T]): The node to check.

        Returns:
            bool: True if the given node is internal, False otherwise.

        Examples:

            >>> tree = Tree()
            >>>
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        return node.is_internal()
    
    def is_branch(self, node: N[T]) -> bool:
        """
        Returns True if the given node is a branch, False otherwise.

        Args:
            node (N[T]): The node to check.
        
        Returns:
            bool: True if the given node is a branch, False otherwise.

        Examples:

            >>> tree = Tree()
            >>>
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        return node.is_branch()
    
    def preorder_traversal(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree in preorder traversal order.
        
        Args:
            node (N[T], optional): The node to start the traversal from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.
            
        Returns:
            list[N[T]]: The nodes of the tree in preorder traversal order.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.preorder_traversal()
            []
            >>> tree = Tree(1)
            >>> tree.preorder_traversal()
            [1]
            >>> tree = Tree(Node(1))
            >>> tree.preorder_traversal()
            [1]
            >>> tree = Tree(Node(1, [Node(2), Node(3)]))
            >>> tree.preorder_traversal()
            [1, 2, 3]
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        nodes = node.preorder_traversal()

        if return_as_node:
            return nodes
        else:
            return [node.get_identity() for node in nodes]

    def postorder_traversal(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree in postorder traversal order.
        
        Args:
            node (N[T], optional): The node to start the traversal from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.
            
        Returns:
            list[N[T]]: The nodes of the tree in postorder traversal order.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.postorder_traversal()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        nodes = node.postorder_traversal()

        if return_as_node:
            return nodes
        else:
            return [node.get_identity() for node in nodes]

    def inorder_traversal(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree in inorder traversal order.
        
        Args:
            node (N[T], optional): The node to start the traversal from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.
            
        Returns:
            list[N[T]]: The nodes of the tree in inorder traversal order.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.inorder_traversal()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        nodes = node.inorder_traversal()

        if return_as_node:
            return nodes
        else:
            return [node.get_identity() for node in nodes]

    def breadth_first_traversal(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree in breadth first traversal order.
        
        Args:
            node (N[T], optional): The node to start the traversal from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.
            
        Returns:
            list[N[T]]: The nodes of the tree in breadth first traversal order.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.breadth_first_traversal()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        nodes = node.breadth_first_traversal()

        if return_as_node:
            return nodes
        else:
            return [node.get_identity() for node in nodes]
    
    def depth_first_traversal(self, node: N[T] = None, return_as_type: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree in depth first traversal order.
        
        Args:
            node (N[T], optional): The node to start the traversal from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.
            
        Returns:
            list[N[T]]: The nodes of the tree in depth first traversal order.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.depth_first_traversal()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        nodes = node.depth_first_traversal()

        if return_as_type:
            return nodes
        else:
            return [node.get_identity() for node in nodes]


    def get_siblings(self, node: N[T], return_as_node) -> list[N[T]]:
        """
        Returns the siblings of the given node.

        Args:
            node (N[T]): The node whose siblings are to be returned.
            return_as_node (bool): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The siblings of the given node.

        Examples:

            >>> tree = Tree()
            >>> tree.get_siblings(1)
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        siblings = node.get_siblings()

        if return_as_node:
            return siblings
        else:
            return [sibling.get_identity() for sibling in siblings]


    def get_ancestors(self, node: N[T], return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the ancestors of the given node.
        
        Args:
            node (N[T]): The node whose ancestors are to be returned.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.
            
        Returns:
            list[N[T]]: The ancestors of the given node.
            
        Examples:
        
            >>> tree = Tree()
            >>> tree.get_ancestors(1)
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        ancestors = node.get_ancestors()

        if return_as_node:
            return ancestors
        else:
            return [ancestor.get_identity() for ancestor in ancestors]

    def get_descendants(self, node: N[T], return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the descendants of the given node.

        Args:
            node (N[T]): The node whose descendants are to be returned.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The descendants of the given node.

        Examples:

            >>> tree = Tree()
            >>> tree.get_descendants(1)
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)

        descendants = node.get_descendants()

        if return_as_node:
            return descendants
        else:
            return [descendant.get_identity() for descendant in descendants]

    def lowest_common_ancestor(self, node1: N[T], node2: N[T], return_as_node: bool = False) -> N[T]:
        """
        Returns the lowest common ancestor of the given nodes.
        
        Args:

            node1 (N[T]): The first node.
            node2 (N[T]): The second node.
            return_as_node (bool, optional): If True, the lowest common ancestor node is returned. If False, the identity of the lowest common ancestor node is returned. Defaults to False.

        Returns:
            N[T]: The lowest common ancestor of the given nodes.

        Examples:
            
                >>> tree = Tree()
                >>> tree.lowest_common_ancestor(1, 2)
                1
        """
        if node1 is None:
            node1 = self.root
        elif isinstance(node1, Node):
            node1 = node1
        else:
            node1 = Node[T](identity=node1)

        if node2 is None:
            node2 = self.root
        elif isinstance(node2, Node):
            node2 = node2
        else:
            node2 = Node[T](identity=node2)

        lca = node1.lowest_common_ancestor(node2)

        if return_as_node:
            return lca
        else:
            return lca.get_identity()

    def get_path(self, node1: N[T], node2: N[T], return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the path from node1 to node2.
        
        Args:

            node1 (N[T]): The first node.
            node2 (N[T]): The second node.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The path from node1 to node2.

        Examples:
                
            >>> tree = Tree()
            >>> tree.get_path(1, 2)
            [1, 2]
        """
        if node1 is None:
            node1 = self.root
        elif isinstance(node1, Node):
            node1 = node1
        else:
            node1 = Node[T](identity=node1)

        if node2 is None:
            node2 = self.root
        elif isinstance(node2, Node):
            node2 = node2
        else:
            node2 = Node[T](identity=node2)

        path = node1.get_path(node2)

        if return_as_node:
            return path
        else:
            return [node.get_identity() for node in path]

    def get_distance(self, node1: N[T], node2: N[T]) -> int:
        """
        Returns the distance between node1 and node2.

        Args:
            
                node1 (N[T]): The first node.
                node2 (N[T]): The second node.

        Returns:
            int: The distance between node1 and node2.

        Examples:

            >>> tree = Tree()
            >>> tree.get_distance(1, 2)
            1
        """
        if node1 is None:
            node1 = self.root
        elif isinstance(node1, Node):
            node1 = node1
        else:
            node1 = Node[T](identity=node1)

        if node2 is None:
            node2 = self.root
        elif isinstance(node2, Node):
            node2 = node2
        else:
            node2 = Node[T](identity=node2)
        
        return node1.get_distance(node2)

    def get_subtree(self, node: N[T]) -> Self[T]:
        """
        Returns the subtree rooted at the given node.

        Args:
            node (N[T]): The node to start the subtree from.

        Returns:
            Tree[T]: The subtree rooted at the given node.

        Examples:

            >>> tree = Tree()
            >>> tree.get_subtree(1)
            Tree(1)
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        return Tree[T](root=node)
    
    def contains_subtree(self, subtree: Self[T]) -> bool:
        """
        Returns True if the tree contains the given subtree, False otherwise.

        Args:
            subtree (Tree[T]): The subtree to check.

        Returns:
            bool: True if the tree contains the given subtree, False otherwise.

        Examples:

            >>> tree = Tree()
            >>> tree.contains_subtree(Tree(1))
            False
        """
        return subtree.get_root() in self.get_nodes()
    
    def clear(self):
        """
        Clears the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.clear()
            >>> tree.is_empty()
            True
        """
        self.root = None

    def copy(self) -> Self[T]:
        """
        Returns a copy of the tree.

        Returns:
            Tree[T]: A copy of the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.copy()
            Tree()
        """
        return Tree[T](root=self.root.copy())
    
    def to_list(self, traversal_type: str = "preorder", return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree in the given traversal order.

        Args:
            traversal_type (str, optional): The traversal order. Defaults to "preorder".
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The nodes of the tree in the given traversal order.

        Examples:

            >>> tree = Tree()
            >>> tree.to_list()
            []
        """
        if traversal_type == "preorder":
            return self.preorder_traversal(return_as_node=return_as_node)
        elif traversal_type == "postorder":
            return self.postorder_traversal(return_as_node=return_as_node)
        elif traversal_type == "inorder":
            return self.inorder_traversal(return_as_node=return_as_node)
        elif traversal_type == "breadth_first":
            return self.breadth_first_traversal(return_as_node=return_as_node)
        elif traversal_type == "depth_first":
            return self.depth_first_traversal(return_as_node=return_as_node)
        else:
            raise ValueError(f"Traversal type {traversal_type} is not supported.")
        
    def prune(self, node: N[T]):
        """
        Prunes the given node from the tree.

        Args:
            node (N[T]): The node to prune.

        Examples:

            >>> tree = Tree()
            >>> tree.prune(1)
            >>> tree.is_empty()
            True
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        node.prune()

    def graft(self, node: N[T], tree: Self[T]):
        """
        Grafts the given tree onto the given node.

        Args:
            node (N[T]): The node to graft onto.
            tree (Tree[T]): The tree to graft.

        Examples:

            >>> tree = Tree()
            >>> tree.graft(1, Tree(2))
            >>> tree.to_list()
            [1, 2]
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        node.add_child(tree.get_root())

    def graft_all(self, node: N[T], trees: list[Self[T]]):
        """
        Grafts the given trees onto the given node.

        Args:
            node (N[T]): The node to graft onto.
            trees (list[Tree[T]]): The trees to graft.

        Examples:

            >>> tree = Tree()
            >>> tree.graft_all(1, [Tree(2), Tree(3)])
            >>> tree.to_list()
            [1, 2, 3]
        """
        for tree in trees:
            self.graft(node, tree)
    
    def get_leaves(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the leaves of the tree.

        Args:
            node (N[T], optional): The node to start the search from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The leaves of the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.get_leaves()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        leaves = node.get_leaves()

        if return_as_node:
            return leaves
        else:
            return [leaf.get_identity() for leaf in leaves]
        
    def get_nodes(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the nodes of the tree.

        Args:
            node (N[T], optional): The node to start the search from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The nodes of the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.get_nodes()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        nodes = node.get_nodes()

        if return_as_node:
            return nodes
        else:
            return [node.get_identity() for node in nodes]
        
    def get_branches(self, node: N[T] = None, return_as_node: bool = False) -> list[N[T]]:
        """
        Returns the branches of the tree.

        Args:
            node (N[T], optional): The node to start the search from. Defaults to None.
            return_as_node (bool, optional): If True, the nodes are returned. If False, the identities of the nodes are returned. Defaults to False.

        Returns:
            list[N[T]]: The branches of the tree.

        Examples:

            >>> tree = Tree()
            >>> tree.get_branches()
            []
        """
        if node is None:
            node = self.root
        elif isinstance(node, Node):
            node = node
        else:
            node = Node[T](identity=node)
        
        branches = node.get_branches()

        if return_as_node:
            return branches
        else:
            return [branch.get_identity() for branch in branches]