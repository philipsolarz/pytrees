from typing import Any, Self

class Node[T]:
    """
    A simple tree node that contains identity and can have multiple children.

    Attributes:
        parent (Node[T], optional): A reference to the parent node. Default is None.
        identity (T, optional): The identity of the node. Default is None.
        children (list[Node[T]], optional): A list of child nodes. Default is an empty list.
    """
    
    def __init__(self, parent: Self = None, identity: T = None, children: list[Self] = []):
        """
        Initialize the Node with optional parent, identity, and children.
        
        Args:
            parent (Node[T], optional): The parent of this node. Defaults to None.
            identity (T, optional): The identity for this node. Defaults to None.
            children (list[Node[T]], optional): The children of this node. Defaults to an empty list.
        """
        self.parent = parent
        self.identity = identity
        self.children = children

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        """Return the identity of this node."""
        return self.identity
    
    def __str__(self) -> str:
        """Return the string representation of this node."""
        return str(self.identity)
    
    def __repr__(self) -> str:
        """Return the string representation of this node."""
        return repr(self.identity)
    
    def __eq__(self, other: Self) -> bool:
        """Return True if the identity of this node is equal to the identity of the other node, otherwise False."""
        return self.identity == other.identity
    
    def __ne__(self, other: Self) -> bool:
        """Return True if the identity of this node is not equal to the identity of the other node, otherwise False."""
        return self.identity != other.identity
    
    def __lt__(self, other: Self) -> bool:
        """Return True if the identity of this node is less than the identity of the other node, otherwise False."""
        return self.identity < other.identity
    
    def __le__(self, other: Self) -> bool:
        """Return True if the identity of this node is less than or equal to the identity of the other node, otherwise False."""
        return self.identity <= other.identity
    
    def __gt__(self, other: Self) -> bool:
        """Return True if the identity of this node is greater than the identity of the other node, otherwise False."""
        return self.identity > other.identity
    
    def __ge__(self, other: Self) -> bool:
        """Return True if the identity of this node is greater than or equal to the identity of the other node, otherwise False."""
        return self.identity >= other.identity
    


    def get_parent(self) -> Self:
        """Return the parent of this node."""
        return self.parent
    
    def set_parent(self, parent: Self) -> None:
        """
        Set the parent for this node.

        Args:
            parent (Node[T]): The parent to set for this node.
        """
        self.parent = parent

    def is_root(self) -> bool:
        """Return True if this node does not have a parent, otherwise False."""
        return self.parent is None
    
    def get_identity(self) -> T:
        """Return the identity of this node."""
        return self.identity
    
    def set_identity(self, identity: T) -> None:
        """
        Set the identity for this node.

        Args:
            identity (T): The identity to set for this node.
        """
        self.identity = identity

    def is_empty(self) -> bool:
        """Return True if this node does not contain any identity, otherwise False."""
        return self.identity is None
    
    def get_children(self) -> list[Self]:
        """Return the list of children for this node."""
        return self.children
    
    def set_children(self, children: list[Self]) -> None:
        """
        Set the children for this node.

        Args:
            children (list[Node[T]]): The list of children to set for this node.
        """
        self.children = children

    def has_children(self) -> bool:
        """Return True if this node has one or more children, otherwise False."""
        return len(self.children) > 0
    
    def add_child(self, child: Self) -> None:
        """
        Add a child to this node.

        Args:
            child (Node[T]): The child to add to this node.
        """
        self.children.append(child)

    def remove_child(self, child: Self) -> None:
        """
        Remove a child from this node.

        Args:
            child (Node[T]): The child to remove from this node.
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
        """Return the number of children for this node."""
        return len(self.children)
    
    def get_descendants(self) -> list[Self]:
        """Return a list of all descendants for this node."""
        descendants = []
        for child in self.children:
            descendants.append(child)
            descendants.extend(child.get_descendants())
        return descendants
    
    def count_descendants(self) -> int:
        """Return the number of descendants for this node."""
        return len(self.get_descendants())
    
    def get_ancestors(self) -> list[Self]:
        """Return a list of all ancestors for this node."""
        ancestors = []
        if self.parent is not None:
            ancestors.append(self.parent)
            ancestors.extend(self.parent.get_ancestors())
        return ancestors
    
    def count_ancestors(self) -> int:
        """Return the number of ancestors for this node."""
        return len(self.get_ancestors())
    
    def get_siblings(self) -> list[Self]:
        """Return a list of all siblings for this node."""
        siblings = []
        if self.parent is not None:
            siblings.extend(self.parent.get_children())
            siblings.remove(self)
        return siblings
    
    def count_siblings(self) -> int:
        """Return the number of siblings for this node."""
        return len(self.get_siblings())
    
    def has_siblings(self) -> bool:
        """Return True if this node has one or more siblings, otherwise False."""
        return self.count_siblings() > 0
    
    def get_leaves(self) -> list[Self]:
        """Return a list of all leaves for this node."""
        leaves = []
        if not self.has_children():
            leaves.append(self)
        else:
            for child in self.children:
                leaves.extend(child.get_leaves())
        return leaves
    
    def count_leaves(self) -> int:
        """Return the number of leaves for this node."""
        return len(self.get_leaves())
    
    def has_leaves(self) -> bool:
        """Return True if this node has one or more leaves, otherwise False."""
        return self.count_leaves() > 0
    
    def get_level(self) -> int:
        """Return the level of this node."""
        level = 0
        if self.parent is not None:
            level = self.parent.get_level() + 1
        return level
    
    def get_height(self) -> int:
        """Return the height of this node."""
        height = 0
        if self.has_children():
            for child in self.children:
                height = max(height, child.get_height() + 1)
        return height
    
    def get_depth(self) -> int:
        """Return the depth of this node."""
        depth = 0
        if self.parent is not None:
            depth = self.parent.get_depth() + 1
        return depth
    

