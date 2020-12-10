import unittest

class Xmas:
    def __init__(self, p, l):
        self.p = p
        self.l = l

    def get_first_fail(self):
        for i in range(self.p, len(self.l)):
            ok = False
            for j in range(self.p):
                for k in range(self.p):
                    a = self.l[i - j - 1]
                    b = self.l[i - k - 1]
                    if a != b and a + b == self.l[i]:
                        ok = True
            if not ok:
                return self.l[i]

    def find_sub(self, x):
        for i in range(len(self.l)):
            j = i
            s = 0
            while j < len(self.l) and s < x:
                s += self.l[j]
                j += 1
            if s == x:
                return self.l[i:j]


class TestXmas(unittest.TestCase):
    def test_get_first_fail(self):
        x = Xmas(5, [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576])
        self.assertEqual(x.get_first_fail(), 127)

    def test_find_sub(self):
        x = Xmas(5, [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576])
        self.assertEqual(x.find_sub(127), [15, 25, 47, 40])


#unittest.main()

l = []
while True:
    try:
        x = input()
    except:
        break
    l.append(int(x))
xmas = Xmas(25, l)
f = xmas.get_first_fail()
print(f)
z = xmas.find_sub(f)
print(min(z) + max(z))
