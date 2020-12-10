import unittest

class Jolts:
    def __init__(self, l):
        self.l = l

    def get_diffs(self):
        l = [0] + sorted(self.l)
        l.append(l[-1] + 3)
        d = {}
        for i in range(len(l) - 1):
            dd = l[i + 1] - l[i]
            if dd not in d:
                d[dd] = 0
            d[dd] += 1
        return d

    def count(self):
        l = [0] + sorted(self.l)
        l.append(l[-1] + 3)
        res = [0] * len(l)
        res[0] = 1
        for i in range(len(l) - 1):
            for j in range(1, 4):
                if i + j < len(l) and l[i + j] - l[i] <= 3:
                    res[i + j] += res[i]
        return res[-1]


class TestJolts(unittest.TestCase):
    def test_get_diffs(self):
        j = Jolts([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
        self.assertEqual(j.get_diffs(), {1: 7, 3: 5})
        j = Jolts([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3])
        self.assertEqual(j.get_diffs(), {1: 22, 3: 10})

    def test_count(self):
        j = Jolts([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4])
        self.assertEqual(j.count(), 8)
        j = Jolts([28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3])
        self.assertEqual(j.count(), 19208)


#unittest.main()

l = []
while True:
    try:
        x = input()
    except:
        break
    l.append(int(x))
j = Jolts(l)
d = j.get_diffs()
print(d)
print(d[1] * d[3])
print(j.count())
