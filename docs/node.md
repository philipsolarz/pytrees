Node Module Documentation
This module defines a Node class that represents a tree node with identity and ability to have multiple children.

Class Node[T]
A simple tree node that contains an identity and can have multiple children.

Attributes:
parent (Node[T], optional): A reference to the parent node. Default is None.
identity (T, optional): The identity of the node. Default is None.
children (list[Node[T]], optional): A list of child nodes. Default is an empty list.
Methods:
__init__(self, parent: Self = None, identity: T = None, children: list[Self] = [])
Initializes the Node with optional parent, identity, and children.

__call__(self, *args: Any, **kwargs: Any) -> T
Returns the identity of this node.

__str__(self) -> str
Returns the string representation of this node.

__repr__(self) -> str
Returns the string representation of this node.

__eq__(self, other: Self) -> bool
Returns True if the identity of this node is equal to the identity of the other node, otherwise False.

__ne__(self, other: Self) -> bool
Returns True if the identity of this node is not equal to the identity of the other node, otherwise False.

Comparison methods:
__lt__: Less than comparison.
__le__: Less than or equal to comparison.
__gt__: Greater than comparison.
__ge__: Greater than or equal to comparison.
Parent methods:
get_parent(): Return the parent of this node.
set_parent(parent: Self): Set the parent for this node.
is_root(): Return True if this node does not have a parent, otherwise False.
Identity methods:
get_identity(): Return the identity of this node.
set_identity(identity: T): Set the identity for this node.
is_empty(): Return True if this node does not contain any identity, otherwise False.
Children methods:
get_children(): Return the list of children for this node.
set_children(children: list[Self]): Set the children for this node.
has_children(): Return True if this node has one or more children, otherwise False.
add_child(child: Self): Add a child to this node.
remove_child(child: Self): Remove a child from this node.
get_child(index: int): Return the child at the specified index.
count_children(): Counts the number of children for this node.
Descendants and Ancestors:
get_descendants(): Return a list of all descendants for this node.
count_descendants(): Return the number of descendants for this node.
get_ancestors(): Return a list of all ancestors for this node.
count_ancestors(): Return the number of ancestors for this node.
Siblings:
get_siblings(): Return a list of all siblings for this node.
count_siblings(): Return the number of siblings for this node.
has_siblings(): Return True if this node has one or more siblings, otherwise False.
Leaves:
get_leaves(): Return a list of all leaves for this node.
count_leaves(): Return the number of leaves for this node.
has_leaves(): Return True if this node has one or more leaves, otherwise False.
Tree Properties:
get_level(): Return the level of this node.
get_height(): Return the height of this node.
get_depth(): Return the depth of this node.
is_leaf(): Return True if this node is a leaf, otherwise False.
is_branch(): Return True if this node is a branch, otherwise False.
is_internal(): Return True if this node is internal, otherwise False.
Traversal methods:
preorder_traversal(): Return a list of nodes in preorder traversal.
postorder_traversal(): Return a list of nodes in postorder traversal.
inorder_traversal(): Return a list of nodes in inorder traversal.
breadth_first_traversal(): Return a list of nodes in breadth-first traversal.
depth_first_traversal(): Return a list of nodes in depth-first traversal.
Other methods:
lowest_common_ancestor(node: Self): Return the lowest common ancestor of this node and the specified node.
get_path(node: Self): Return the path from this node to the specified node.
get_distance(node: Self): Return the distance from this node to the specified node.
prune(): Remove all children from this node.
clear(): Remove all children from this node and set the identity to None.
copy(): Return a copy of this node.
deepcopy(): Return a deepcopy of this node.