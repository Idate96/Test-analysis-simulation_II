'testing unittest'
import unittest

def prime(num):
    num=input('enter integer number: ')

    a=[]
    b=[]


    if num > 1:
        for i in xrange(2,num/2+1,2):
            if num % i == 0:
                a.append(i)

    for n in a:
        x = True
        for h in xrange(2,n):
            if n % h == 0:
                x = False
        if x == True:
            b.append(n)

    return a

class Testprimes(unittest.TestCase):
    def test(self):