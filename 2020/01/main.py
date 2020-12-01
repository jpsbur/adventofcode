import unittest

class ExpenseReport:

    def find_pair(self, l, s):
        """Find pair of numbers in list l that sum to s."""
        for x in l:
            for y in l:
                if x + y == s:
                    return x, y

    def find_triple(self, l, s):
        """Find triple of numbers in list l that sum to s."""
        for x in l:
            for y in l:
                for z in l:
                    if x + y + z == s:
                        return x, y, z


class TestExpenseReport(unittest.TestCase):

    def test_find_pair(self):
        e = ExpenseReport()
        l = [1721, 979, 366, 299, 675, 1456]
        s = 2020
        x, y = e.find_pair(l, s)
        self.assertEqual(s, x + y)
        self.assertTrue(x in l)
        self.assertTrue(y in l)

    def test_find_triple(self):
        e = ExpenseReport()
        l = [1721, 979, 366, 299, 675, 1456]
        s = 2020
        x, y, z = e.find_triple(l, s)
        self.assertEqual(s, x + y + z)
        self.assertTrue(x in l)
        self.assertTrue(y in l)
        self.assertTrue(z in l)


#unittest.main()

l = []
while True:
    try:
        x = int(input())
        l.append(x)
    except:
        break
e = ExpenseReport()
x, y = e.find_pair(l, 2020)
print(x * y)
x, y, z = e.find_triple(l, 2020)
print(x * y * z)
