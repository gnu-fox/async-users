class User:
    def __init__(self, id : int):
        self.id = id


class Context:
    users = set()

    def __init__(self):
        self.user1 : User = User(id=None)
        self.user2 : User = User(id=None)

        self.users.add(self.user1)
        self.users.add(self.user2)

    def change_user(self):
        self.user1.__init__(id=3)
        self.user2.__init__(id=4)



users = Context()


for user in users.users:
    print(user)

users.change_user()

for user in users.users:
    print(user)

copy = users.user1
copy.id = 5


for user in users.users:
    print(user.id)
