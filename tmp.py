class Account:
    def __init__(self, id):
        self.id = id

    def __repr__(self) -> str:
        return f"Account(id={self.id})"

account1 = Account(id=1)
account2 = Account(id=2)
account3 = Account(id=3)

account4 = Account(id=4)
account5 = Account(id=5)
account6 = Account(id=6)

set1 = {account1, account2, account3}
set2 = {account4, account5, account6}

set1.update(set2)
set2.clear()

print(set1)
print(set2)