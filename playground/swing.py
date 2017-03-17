import pdb

def first(lst):
    return lst[0]

lst = [0,1,2]



print(first(lst))


class TestStringMethods(unittest.testcase):
    def testfirst(self):
        self.assertequal(first(lst,1))
