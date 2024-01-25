class Account:
    def __init__(self, id : int):
        self.id = id


dict1 = {
    'account_1' : Account(id=1),
    'account_2' : Account(id=2),
}

dict2 = dict1

dict1['account_1'].id = 3

print(dict2['account_1'].id)