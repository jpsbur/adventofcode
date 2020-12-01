import unittest

class ExpenseReport:

    def find_sum(self, l, s):
        """Find pair of numbers in list l that sum to s."""
        for x in l:
            for y in l:
                if x + y == s:
                    return x, y


class TestExpenseReport(unittest.TestCase):

    def test_find_sum(self):
        e = ExpenseReport()
        l = [1721, 979, 366, 299, 675, 1456]
        s = 2020
        x, y = e.find_sum(l, s)
        self.assertEqual(s, x + y)
        self.assertTrue(x in l)
        self.assertTrue(y in l)


#unittest.main()

l = []
while True:
    try:
        x = int(input())
        l.append(x)
    except:
        break
e = ExpenseReport()
x, y = e.find_sum(l, 2020)
print(x * y)
