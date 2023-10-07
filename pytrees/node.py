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
        return self.identity
    
    def __str__(self) -> str:
        return str(self.identity)
    
    def __repr__(self) -> str:
        return repr(self.identity)

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
