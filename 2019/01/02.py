import unittest

class Fuel:
    def get_fuel(self, x):
        res = 0
        while True:
            x = x // 3 - 2
            if x < 0:
                break
            res += x
        return res


class TestFuel(unittest.TestCase):

    def test_get_fuel(self):
        f = Fuel()
        self.assertEqual(2, f.get_fuel(14))
        self.assertEqual(966, f.get_fuel(1969))



#unittest.main()

f = Fuel()
res = 0
while True:
    try:
        s = input()
    except:
        break
    a = int(s)
    res += f.get_fuel(a)
print(res)
