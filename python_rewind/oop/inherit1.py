# Python Multi-Level inheritance
class Summation:
    def __init__(self,number1,number2,number3):
        self.no1 = number1
        self.no2 = number2
        self.no3 = number3
    def sum(self):
        return self.no1 + self.no2 + self.no3

class Multi(Summation):
    def __init__(self,number1,number2,number3,number4):
        super().__init__(number1,number2,number3)
        self.no4 = number4

    def multi(self):
        return self.no1 * self.no2 * self.no3 * self.no4

class MultiSum(Multi):
    def __init__(self,number1,number2,number3,number4):
        super().__init__(number1,number2,number3,number4)

    def multiSum(self):
        return (self.no1 * self.no4) + (self.no2 * self.no3)


if __name__ == '__main__':
    obj1 = MultiSum(1,2,3,4)

    print(obj1.sum())
    print(obj1.multi())
    print(obj1.multiSum())