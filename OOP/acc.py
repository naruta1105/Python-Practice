class Account :
    def __init__(self,filepath):
        with open(filepath) as myfile :
            self.balance = int(myfile.read())