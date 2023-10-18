from experimental.simpletree import Tree

class Session:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f'Session: {self.name}'
    
    def func(self):
        print("Hello World!")

class Console[T](Tree[T]):
    def __init__(self, root):
        super().__init__(root)


root = Session("root")

console = Console[Session](root)

console.root.identity.func()

print(str(console.root.identity))

print(console.is_empty())

print(str(console.root().func()))

