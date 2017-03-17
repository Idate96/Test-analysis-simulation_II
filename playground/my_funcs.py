"""Examples of unitttest"""
import unittest


def my_func(x,y):
    """This fuction devides two number.

    Args:
        x (int) = number 1
        y (int) = number 2

    Returns:
        div (int) = division of number
    """
    assert(y!=0), "No division by 0"
    return int(x/y)


# test
class Test_my_func(unittest.TestCase):

    def test_1(self):
        """Test my_func with built-in"""
        for i in range(1,10):
            self.assertAlmostEqual(my_func(i,i**2), i/i**2, places=10)


    def test_2(self):
        for i in range(1,10):
            self.assertAlmostEqual(my_func(i,i**2), int(i/i**2), places=10)





if __name__ == '__main__':
    unittest.main()
