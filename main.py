# from experimental.simpletree import Tree
from pytrees.tree import Tree, TraversalType
from pytrees.node import Node
class Session:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'Session: {self.name}'
    
    def func(self):
        print("Hello World!")

class Console[T](Tree[T]):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)


root = Session("root")
tree = Tree[Session](root)
# tree.pprint()
b1 = Session("branch1")
tree.add_branch(b1)
#branch1 = tree.root.branches[0]
#print(branch1.branches[0].identity.name)

# tree.root.branches[0].display_tree()
tree.print()
tree.add_branch(Session("branch2"), source=lambda source: source.identity.name == "branch1", traversal_type=TraversalType.PREORDER)
tree.print()



tree2 = Tree[Session].from_dict({
    "identity": root,
    "branches": [
        {
            "identity": Session("branch1"),
            "branches": [
                {
                    "identity": Session("branch1.1"),
                    "branches": [
                        {
                            "identity": Session("branch1.1.1"),
                            "branches": []
                        },
                        {
                            "identity": Session("branch1.1.2"),
                            "branches": []
                        }
                    ]
                },
                {
                    "identity": Session("branch1.2"),
                    "branches": []
                }
            ]
        },
        {
            "identity": Session("branch2"),
            "branches": []
        }
    ]
})
tree2.print()
