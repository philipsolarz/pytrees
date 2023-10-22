
class Foo:
    def __init__(self, name, lst = []):
        self.name = name
        self.lst = lst

    def add(self, other):
        self.lst.append(other.name)

class Bar:
    def __init__(self):
        pass

    def add_foo(self, foo1, foo2):
        foo1.add(foo2)

foo1 = Foo("foo1")
foo2 = Foo("foo2")
bar = Bar()
bar.add_foo(foo1, foo2)
print(foo1.lst)
print(foo2.lst)