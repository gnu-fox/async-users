from typing import Protocol
from abc import ABC, abstractmethod

class absB(Protocol):
    def print(self):
        ...


class absC(Protocol):
    def print(self):
        ...

class A(ABC):
    pass

class B(A):
    def print(self):
        print("B")

class C(A):
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
                

class W(Repo):
    def __init__(self):
        super().__init__()
        self.b : absB
        self.c : absB


class D(W):
    def __init__(self):
        super().__init__()
        self.b = B()

d = D()
d.begin()



class Base(ABC):
    def __init__(self, a : int):
        ...
    

class Derived(Base):
    def __init__(self, a : int):
        self.a = a


m = Derived(1)
print(m.a)
