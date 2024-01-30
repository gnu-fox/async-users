from abc import ABC, abstractmethod

class A(ABC):
    pass

    @abstractmethod
    def print(self):
        ...

class B(A):
    def __init__(self):
        pass

    def print(self):
        print("B")

class C(A):
    def __init__(self):
        pass

    def print(self):
        print("C")


class Repo:
    word = "hello"
    
    def __init__(self):
        self.__word = self.word

    def begin(self):
        for _, attribute_value in self.__dict__.items():
            if isinstance(attribute_value, A):
                print(self.__word)
                attribute_value.print()
                



class D(Repo):
    def __init__(self):
        super().__init__()
        self.b = B()
        self.c = C()


d = D()
d.begin()