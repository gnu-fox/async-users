from abc import ABC, abstractmethod, abstractproperty

class Base(ABC):

    @property
    @abstractmethod
    def age(self) -> int:
        pass


class Derived(Base):
    number : int

    def __init__(self):
        pass

    @property
    def age(self) -> int:
        return self.number
    
    def __enter__(self):
        self.number = 1

    def __exit__(self, exc_type, exc_value, traceback):
        pass


derived = Derived()

with derived:
    print(derived.age)