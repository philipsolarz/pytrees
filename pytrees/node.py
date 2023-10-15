from typing import Any, Self
type C[T] = Self | T | dict[T | list[T]]


class Node[T]:
    """
    A node in a tree.

    Attributes:
        parent (Node[T]): The parent of this node.
        identity (T): The identity of this node.
        children (list[Node[T]]): The children of this node.
        max_children (int | None, optional): The maximum number of children allowed for this node. Defaults to None.

    """
    
    def __init__(self, parent: Self = None, identity: T = None, children: list[Self] = [], max_children: int | None = None) -> None:
        """
        Initialize a new node.

        Args:
            parent (Node[T], optional): The parent of this node. Defaults to None.
            identity (T, optional): The identity of this node. Defaults to None.
            children (list[Node[T]], optional): The children of this node. Defaults to [].
            max_children (int | None, optional): The maximum number of children allowed for this node. Defaults to None.
        """
        self.parent = parent
        self.identity = identity

        if max_children is not None:
            if len(children) > max_children:
                raise ValueError(f"Number of children ({len(children)}) cannot exceed maximum number of children ({max_children}).")
        self.children = children

    def __repr__(self) -> str:
        """
        Return the string representation of this node.

        Returns:
            str: The string representation of this node.
        """
        return f"Node({self.parent}, {self.identity}, {self.children})"
    
    def __str__(self) -> str:
        """
        Return the string representation of this node.
        
        Returns:
            str: The string representation of this node.
        """
        return str(self.identity)
    
    def __eq__(self, other: Self) -> bool:
        """
        Return True if the depth of this node is equal to the depth of the other node, otherwise False.

        Args:
            other (N[T]): The other node to compare with.

        Returns:
            bool: True if the depth of this node is equal to the depth of the other node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 == node2
            True
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 == node2
            False
        """
        return self.get_depth == other.get_depth

    def __ne__(self, other: Self) -> bool:
        """
        Return True if the depth of this node is not equal to the depth of the other node, otherwise False.

        Args:
            other (N[T]): The other node to compare with.

        Returns:
            bool: True if the depth of this node is not equal to the depth of the other node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 != node2
            False
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 != node2
            True
        """
        return self.get_depth != other.get_depth
    
    def __lt__(self, other: Self) -> bool:
        """
        Return True if the depth of this node is less than the depth of the other node, otherwise False.

        Args:
            other (N[T]): The other node to compare with.

        Returns:
            bool: True if the depth of this node is less than the depth of the other node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 < node2
            False
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 < node2
            True
        """
        return self.get_depth < other.get_depth
    
    def __le__(self, other: Self) -> bool:
        """
        Return True if the depth of this node is less than or equal to the depth of the other node, otherwise False.

        Args:
            other (N[T]): The other node to compare with.

        Returns:
            bool: True if the depth of this node is less than or equal to the depth of the other node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 <= node2
            True
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 <= node2
            True
        """
        return self.get_depth <= other.get_depth
    
    def __gt__(self, other: Self) -> bool:
        """
        Return True if the depth of this node is greater than the depth of the other node, otherwise False.

        Args:
            other (N[T]): The other node to compare with.

        Returns:
            bool: True if the depth of this node is greater than the depth of the other node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 > node2
            False
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 > node2
            False
        """
        return self.get_depth > other.get_depth
    
    def __ge__(self, other: Self) -> bool:
        """
        Return True if the depth of this node is greater than or equal to the depth of the other node, otherwise False.

        Args:
            other (N[T]): The other node to compare with.

        Returns:
            bool: True if the depth of this node is greater than or equal to the depth of the other node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 >= node2
            True
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 >= node2
            False
        """
        return self.get_depth >= other.get_depth
    
    def __contains__(self, node: Self) -> bool:
        """
        Return True if the specified node is a descendant of this node, otherwise False.

        Args:
            node (Node[T]): The node to check.

        Returns:
            bool: True if the specified node is a descendant of this node, otherwise False.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1 in node2
            False
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1 in node2
            True
        """
        return node in self.get_descendants()
    
    def __len__(self) -> int:
        """
        Return the number of children for this node.

        Returns:
            int: The number of children for this node.

        Examples:
            >>> node = Node()
            >>> len(node)
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> len(node)
            1
        """
        return len(self.children)

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """
        Return the identity of this node.

        Returns:
            T: The identity of this node.

        Examples:
            >>> node = Node()
            >>> node()
            None
            >>> node = Node(None, "A")
            >>> node()
            'A'
        """
        return self.identity

    def get_parent(self) -> Self:
        """
        Return the parent of this node.
        
        Returns:
            Node[T]: The parent of this node.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1.get_parent()
            Node(None, None, [Node(None, None, [Node(None, None, [])])])
        """
        return self.parent
    
    def set_parent(self, parent: Self) -> None:
        """
        Set the parent for this node.

        Args:
            parent (Node[T]): The parent to set for this node.

        Examples:
            >>> node1 = Node()
            >>> node2 = Node()
            >>> node1.set_parent(node2)
            >>> node1.get_parent()
            Node(None, None, [Node(None, None, [Node(None, None, [])])])
        """
        self.parent = parent

    def is_root(self) -> bool:
        """
        Return True if this node does not have a parent, otherwise False.
        
        Returns:
            bool: True if this node does not have a parent, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.is_root()
            True
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.is_root()
            False
        """
        return self.parent is None
    
    def get_identity(self) -> T:
        """
        Return the identity of this node.
        
        Returns:
            T: The identity of this node.
            
        Examples:
            >>> node = Node()
            >>> node.get_identity()
            None
            >>> node = Node(None, "A")
            >>> node.get_identity()
            'A'
        """
        return self.identity
    
    def set_identity(self, identity: T) -> None:
        """
        Set the identity for this node.

        Args:
            identity (T): The identity to set for this node.

        Examples:
            >>> node = Node()
            >>> node.set_identity("A")
            >>> node.get_identity()
            'A'
        """
        self.identity = identity

    def is_empty(self) -> bool: # is_anonymous
        """
        Return True if this node does not contain any identity, otherwise False.
        
        Returns:
            bool: True if this node does not contain any identity, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.is_empty()
            True
            >>> node = Node(None, "A")
            >>> node.is_empty()
            False
        """
        return self.identity is None
    
    def get_children(self) -> list[Self]:
        """
        Return the list of children for this node.
        
        Returns:
            list[Node[T]]: The list of children for this node.
            
        Examples:
            >>> node = Node()
            >>> node.get_children()
            []
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_children()
            [Node(None, None, [Node(None, None, [])])]
        """
        return self.children
    
    def set_children(self, children: list[Self]) -> None:
        """
        Set the children for this node.

        Args:
            children (list[Node[T]]): The list of children to set for this node.

        Examples:
            >>> node = Node()
            >>> node.set_children([Node(None, None, [Node(None, None, [])])])
            >>> node.get_children()
            [Node(None, None, [Node(None, None, [])])]
        """
        self.children = children

    def has_children(self) -> bool:
        """
        Return True if this node has one or more children, otherwise False.
        
        Returns:
            bool: True if this node has one or more children, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.has_children()
            False
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.has_children()
            True
        """
        return len(self.children) > 0
    
    def add_child(self, child: Self) -> None:
        """
        Add a child to this node.

        Args:
            child (Node[T]): The child to add to this node.

        Examples:
            >>> node = Node()
            >>> node.add_child(Node(None, None, [Node(None, None, [])]))
            >>> node.get_children()
            [Node(None, None, [Node(None, None, [])])]
        """
        self.children.append(child)

    def remove_child(self, child: Self) -> None:
        """
        Remove a child from this node.

        Args:
            child (Node[T]): The child to remove from this node.

        Examples:
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.remove_child(Node(None, None, [Node(None, None, [])]))
            >>> node.get_children()
            []
        """
        self.children.remove(child)

    def get_child(self, index: int) -> Self:
        """
        Return the child at the specified index.

        Args:
            index (int): The index of the child to return.

        Returns:
            Node[T]: The child at the specified index.
        """
        return self.children[index]
    
    def count_children(self) -> int:
        """Counts the number of children for this node.
        
        Returns:
            int: The number of children for this node.

        Examples:
            >>> node = Node()
            >>> node.count_children()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.count_children()
            1
        """
        return len(self.children)
    
    def get_descendants(self) -> list[Self]:
        """Return a list of all descendants for this node.
        
        Returns:
            list[Node[T]]: A list of all descendants for this node.

        Examples:
            >>> node = Node()
            >>> node.get_descendants()
            []
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_descendants()
            [Node(None, None, [Node(None, None, [])]), Node(None, None, [])]
        """
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def count_descendants(self) -> int:
        """Return the number of descendants for this node.
        
        Returns:
            int: The number of descendants for this node.

        Examples:
            >>> node = Node()
            >>> node.count_descendants()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.count_descendants()
            2
        """
        return len(self.get_descendants())
    
    def get_ancestors(self) -> list[Self]:
        """Return a list of all ancestors for this node.
        
        Returns:
            list[Node[T]]: A list of all ancestors for this node.

        Examples:
            >>> node = Node()
            >>> node.get_ancestors()
            []
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_ancestors()
            [Node(None, None, [Node(None, None, [])])]
        """
        ancestors = []
        if self.parent is not None:
            ancestors.append(self.parent)
            ancestors.extend(self.parent.get_ancestors())
        return ancestors
    
    def count_ancestors(self) -> int:
        """Return the number of ancestors for this node.
        
        Returns:
            int: The number of ancestors for this node.

        Examples:
            >>> node = Node()
            >>> node.count_ancestors()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.count_ancestors()
            1
        """
        return len(self.get_ancestors())
    
    def get_siblings(self) -> list[Self]:
        """Return a list of all siblings for this node.
        
        Returns:
            list[Node[T]]: A list of all siblings for this node.

        Examples:
            >>> node = Node()
            >>> node.get_siblings()
            []
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_siblings()
            []
        """
        siblings = []
        if self.parent is not None:
            siblings.extend(self.parent.get_children())
            siblings.remove(self)
        return siblings
    
    def count_siblings(self) -> int:
        """Return the number of siblings for this node.
        
        Returns:
            int: The number of siblings for this node.

        Examples:
            >>> node = Node()
            >>> node.count_siblings()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.count_siblings()
            0
        """
        return len(self.get_siblings())
    
    def has_siblings(self) -> bool:
        """Return True if this node has one or more siblings, otherwise False.
        
        Returns:
            bool: True if this node has one or more siblings, otherwise False.

        Examples:
            >>> node = Node()
            >>> node.has_siblings()
            False
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.has_siblings()
            False
        """
        return self.count_siblings() > 0
    
    def get_leaves(self) -> list[Self]:
        """Return a list of all leaves for this node.
        
        Returns:
            list[Node[T]]: A list of all leaves for this node.
        
        Examples:
            >>> node = Node()
            >>> node.get_leaves()
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_leaves()
            [Node(None, None, [])]
        """
        leaves = []
        if not self.has_children():
            leaves.append(self)
        else:
            for child in self.children:
                leaves.extend(child.get_leaves())
        return leaves
    
    def count_leaves(self) -> int:
        """
        Return the number of leaves for this node.
        
        Returns:
            int: The number of leaves for this node.
            
        Examples:
            >>> node = Node()
            >>> node.count_leaves()
            1
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.count_leaves()
            1
        """
        return len(self.get_leaves())
    
    def has_leaves(self) -> bool:
        """
        Return True if this node has one or more leaves, otherwise False.
        
        Returns:
            bool: True if this node has one or more leaves, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.has_leaves()
            True
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.has_leaves()
            True
        """
        return self.count_leaves() > 0
    
    def get_level(self) -> int:
        """
        Return the level of this node.
        
        Returns:
            int: The level of this node.
            
        Examples:
            >>> node = Node()
            >>> node.get_level()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_level()
            1
        """
        level = 0
        if self.parent is not None:
            level = self.parent.get_level() + 1
        return level
    
    def get_height(self) -> int:
        """
        Return the height of this node.
        
        Returns:
            int: The height of this node.
            
        Examples:
            >>> node = Node()
            >>> node.get_height()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_height()
            2
        """
        height = 0
        if self.has_children():
            for child in self.children:
                height = max(height, child.get_height() + 1)
        return height
    
    def get_depth(self) -> int:
        """
        Return the depth of this node.
        
        Returns:
            int: The depth of this node.
            
        Examples:
            >>> node = Node()
            >>> node.get_depth()
            0
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.get_depth()
            1
        """
        depth = 0
        if self.parent is not None:
            depth = self.parent.get_depth() + 1
        return depth
    
    def is_leaf(self) -> bool:
        """
        Return True if this node is a leaf, otherwise False.
        
        Returns:
            bool: True if this node is a leaf, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.is_leaf()
            True
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.is_leaf()
            False
        """
        return not self.has_children()
    
    def is_branch(self) -> bool:
        """
        Return True if this node is a branch, otherwise False.
        
        Returns:
            bool: True if this node is a branch, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.is_branch()
            False
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.is_branch()
            True
        """
        return self.has_children()
    
    def is_internal(self) -> bool:
        """
        Return True if this node is internal, otherwise False.
        
        Returns:
            bool: True if this node is internal, otherwise False.
            
        Examples:
            >>> node = Node()
            >>> node.is_internal()
            False
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.is_internal()
            True
        """
        return self.has_children()
    
    def preorder_traversal(self) -> list[Self]:
        """Return a list of nodes in preorder traversal.
        
        Returns:
            list[Node[T]]: A list of nodes in preorder traversal.

        Examples:
            >>> node = Node()
            >>> node.preorder_traversal()
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.preorder_traversal()
            [Node(None, None, [Node(None, None, [Node(None, None, [])])]), Node(None, None, [Node(None, None, [])]), Node(None, None, [])]
        """
        nodes = []
        nodes.append(self)
        for child in self.children:
            nodes.extend(child.preorder_traversal())
        return nodes
    
    def postorder_traversal(self) -> list[Self]:
        """Return a list of nodes in postorder traversal.
        
        Returns:
            list[Node[T]]: A list of nodes in postorder traversal.

        Examples:
            >>> node = Node()
            >>> node.postorder_traversal()
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.postorder_traversal()
            [Node(None, None, []), Node(None, None, [Node(None, None, [])]), Node(None, None, [Node(None, None, [Node(None, None, [])])])]
        """
        nodes = []
        for child in self.children:
            nodes.extend(child.postorder_traversal())
        nodes.append(self)
        return nodes
    
    def inorder_traversal(self) -> list[Self]:
        """Return a list of nodes in inorder traversal.
        
        Returns:
            list[Node[T]]: A list of nodes in inorder traversal.
        
        Examples:
            >>> node = Node()
            >>> node.inorder_traversal()
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.inorder_traversal()
            [Node(None, None, [Node(None, None, [])]), Node(None, None, []), Node(None, None, [Node(None, None, [Node(None, None, [])])])]
        """
        nodes = []
        if self.has_children():
            nodes.extend(self.children[0].inorder_traversal())
        nodes.append(self)
        if self.has_children():
            nodes.extend(self.children[1].inorder_traversal())
        return nodes
    
    def breadth_first_traversal(self) -> list[Self]:
        """Return a list of nodes in breadth-first traversal.
        
        Returns:
            list[Node[T]]: A list of nodes in breadth-first traversal.

        Examples:
            >>> node = Node()
            >>> node.breadth_first_traversal()
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.breadth_first_traversal()
            [Node(None, None, [Node(None, None, [Node(None, None, [])])]), Node(None, None, []), Node(None, None, [Node(None, None, [])]), Node(None, None, [Node(None, None, [])])]
        """
        nodes = []
        queue = [self]
        while len(queue) > 0:
            node = queue.pop(0)
            nodes.append(node)
            queue.extend(node.children)
        return nodes
    
    def depth_first_traversal(self) -> list[Self]:
        """Return a list of nodes in depth-first traversal.
        
        Returns:
            list[Node[T]]: A list of nodes in depth-first traversal.

        Examples:
            >>> node = Node()
            >>> node.depth_first_traversal()
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.depth_first_traversal()
            [Node(None, None, [Node(None, None, [Node(None, None, [])])]), Node(None, None, []), Node(None, None, [Node(None, None, [])]), Node(None, None, [Node(None, None, [])])]
        """
        nodes = []
        stack = [self]
        while len(stack) > 0:
            node = stack.pop()
            nodes.append(node)
            stack.extend(node.children)
        return nodes
    
    def traverse(self, traversal_type: str = "preorder") -> list[Self]:
        """Return a list of nodes in the specified traversal type.
        
        Args:
            traversal_type (str, optional): The traversal type to use. Defaults to "preorder".
        
        Returns:
            list[Node[T]]: A list of nodes in the specified traversal type.

        Examples:
            >>> node = Node()
            >>> node.traverse("preorder")
            [Node(None, None, [])]
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.traverse("preorder")
            [Node(None, None, [Node(None, None, [Node(None, None, [])])]), Node(None, None, [Node(None, None, [])]), Node(None, None, [])]
        """
        if traversal_type == "preorder":
            return self.preorder_traversal()
        elif traversal_type == "postorder":
            return self.postorder_traversal()
        elif traversal_type == "inorder":
            return self.inorder_traversal()
        elif traversal_type == "breadth-first":
            return self.breadth_first_traversal()
        elif traversal_type == "depth-first":
            return self.depth_first_traversal()
        else:
            raise ValueError(f"Traversal type '{traversal_type}' is not supported.")
    
    def lowest_common_ancestor(self, node: Self) -> Self:
        """
        Return the lowest common ancestor of this node and the specified node.

        Args:
            node (Node[T]): The node to find the lowest common ancestor with.

        Returns:
            Node[T]: The lowest common ancestor of this node and the specified node.
        """
        ancestors = self.get_ancestors()
        node_ancestors = node.get_ancestors()
        common_ancestors = [ancestor for ancestor in ancestors if ancestor in node_ancestors]
        return common_ancestors[0]
    
    def get_path(self, node: Self) -> list[Self]:
        """
        Return the path from this node to the specified node.

        Args:
            node (Node[T]): The node to find the path to.

        Returns:
            list[Node[T]]: The path from this node to the specified node.
        """
        path = []
        ancestor = self.lowest_common_ancestor(node)
        while self != ancestor:
            path.append(self)
            self = self.parent
        path.append(ancestor)
        while node != ancestor:
            path.append(node)
            node = node.parent
        return path
    
    def get_distance(self, node: Self) -> int:
        """
        Return the distance from this node to the specified node.

        Args:
            node (Node[T]): The node to find the distance to.

        Returns:
            int: The distance from this node to the specified node.
        """
        path = self.get_path(node)
        return len(path) - 1
    
    def prune(self) -> None:
        """
        Remove all children from this node.

        Examples:
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.prune()
            >>> node.get_children()
            []
        """
        self.children = []

    def clear(self) -> None:
        """
        Remove all children from this node and set the identity to None.
        
        Examples:
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node.clear()
            >>> node.get_children()
            []
            >>> node.get_identity()
            None
        """
        self.children = []
        self.identity = None

    def copy(self) -> Self:
        """
        Return a copy of this node.
        
        Returns:
            Node[T]: A copy of this node.
        
        Examples:
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node_copy = node.copy()
            >>> node_copy
            Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node_copy is node
            False
        """
        return Node(self.parent, self.identity, self.children)
    
    def deepcopy(self) -> Self:
        """
        Return a deepcopy of this node.

        Returns:
            Node[T]: A deepcopy of this node.

        Examples:
            >>> node = Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node_copy = node.deepcopy()
            >>> node_copy
            Node(None, None, [Node(None, None, [Node(None, None, [])])])
            >>> node_copy is node
            False
        """
        return Node(self.parent, self.identity, [child.deepcopy() for child in self.children])
    


