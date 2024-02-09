class inject:
    def __init__(self, secret : str):
        self.secret = secret
    
    def __call__(self, function):
        def wrapper(*args, **kwargs):
            return function(*args, **kwargs, secret = self.secret)
        return wrapper
    

class Tokenizer:
    def __init__(self):
        pass

    @inject(secret="my_secret")
    def encode(self, subject : str, secret : str) -> str:
        print(secret)


tokenizer = Tokenizer()

tokenizer.encode("subject")