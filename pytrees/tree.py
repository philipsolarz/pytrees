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
    
    def get_height(self) -> int:
        return self.root.get_height()
    
    def get_size(self) -> int:
        return self.root.get_size()
    
    def get_leaves(self) -> list[Node[T]]:
        return self.root.get_leaves()
    
    def get_nodes(self) -> list[Node[T]]:
        return self.root.get_nodes()
    
    def get_node(self, identity: T) -> Node[T]:
        return self.root.get_node(identity)
    
    

