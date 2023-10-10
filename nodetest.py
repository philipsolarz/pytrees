from typing import Any, Self
type C[T] = Self | T | dict[T | list[T]]
class Node[T]:
    def __init__(self, parent: Self = None, identity: T = None, children: C[T] = [], max_children: int | None = None) -> None:
        self.parent = parent
        self.identity = identity
        self.max_children = max_children
        self.children = []
        if self.max_children is not None:
            if len(children) > self.max_children:
                raise ValueError(f"Number of children ({len(children)}) cannot exceed maximum number of children ({self.max_children}).")
        for child in children:
            if isinstance(child, Node):
                self.add_child(child)
            elif isinstance(child, dict):
                self.build_subtree_from_dict(child)
            else:
                self.add_child(Node(self, child, max_children=self.max_children))

    def add_child(self, child: Self) -> None:
        if self.max_children is not None:
            if len(self.children) >= self.max_children:
                raise ValueError(f"Number of children ({len(self.children)}) cannot exceed maximum number of children ({self.max_children}).")
        self.children.append(child)
        
    def build_subtree_from_dict(self, subtree: dict) -> None:
        if len(subtree) != 1:
            raise ValueError("There can only be one root node.")
        for key, value in subtree.items():
            child_node = Node(parent=self, identity=key, max_children=self.max_children)
            self.add_child(child_node)
            if value is not None:
                for subtree in value:
                    child_node.build_subtree_from_dict(subtree)

# Example usage
subtree = {
    'A': [{'B': None},
          {'C': [{'E': None}]},
          {'D': [{'F': None}]}
         ]
}
root = Node[str](identity='Root', children=[subtree])

print(root.children)