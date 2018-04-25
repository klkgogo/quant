class AClass(object):
    def p(self):
        print("a")

    def aa(self):
        self.__aa()
        self.bb()

    def __aa(self):
        print("__A")

    def bb(self):
        print("aa")


class BClas(AClass):
    def p(self):
        print("b")

    def __aa(self):
        print("__B")

    def bb(self):
        print("bb")


a = AClass()
b = BClas()
a.p()
a.aa()
a.bb()
b.p()
b.aa()
b.bb()
b._BClas__aa()
print(BClas.__dict__)