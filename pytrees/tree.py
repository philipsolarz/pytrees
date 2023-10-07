from pytrees.node import Node

class Tree[T]:    
    def __init__(self, root: T = None):
        self.root = Node[T](identity=root)

    def get_root(self):
        return self.root
    
    def set_root(self, root: Node[T]):
        self.root = root

    def is_empty(self) -> bool:
        return self.root is None

