import re
class Capital(object):
    def __init__(self,str):
        self.string = str

    def capitalCheck(self):
        if re.search("[A-Z]",self.string):
            return True
        else:
            return False

class Small(Capital):
    def __init__(self,str):
        super().__init__(str)

    def smallCheck(self):
        if re.search("[a-z]",self.string):
            return True
        else:
            return False

class Number(Small):
    def __init__(self,str):
        super().__init__(str)

    def numCheck(self):
        if re.search("[0-9]",self.string):
            return True
        else:
            return False

class Special(Number):
    def __init__(self,str):
        super().__init__(str)

    def checkSpecial(self):
        if re.search("[_@$/|?#]",self.string):
            return True
        else:
            return False

if __name__ == '__main__':
    sp = Special("chirH98")
    sp2 = Special("CHIRU")
    sp3 = Special("goldy#98")
    print(sp.capitalCheck())
    print(sp2.smallCheck())
    print(sp2.numCheck())
    print(sp3.checkSpecial())
    print(sp2.checkSpecial())