import unittest

class Memory:
    def __init__(self, a):
        self.a = list(map(int, a.split(',')))
        self.last = {}
        for i in range(len(self.a) - 1):
            self.last[self.a[i]] = i

    def iterate(self):
        x = self.a[-1]
        i = len(self.a) - 1
        if x in self.last:
            y = i - self.last[x]
        else:
            y = 0
        self.last[x] = i
        self.a.append(y)

    def get(self, i):
        while len(self.a) < i:
            self.iterate()
        return self.a[-1]


class TestMemory(unittest.TestCase):
    def test_get(self):
        tests = [
            ('1,3,2', 1),
            ('2,1,3', 10),
            ('1,2,3', 27),
            ('2,3,1', 78),
            ('3,2,1', 438),
            ('3,1,2', 1836),
        ]
        for t, r in tests:
            m = Memory(t)
            self.assertEqual(m.get(2020), r)

        tests = [
            ('0,3,6', 175594),
            ('1,3,2', 2578),
            ('2,1,3', 3544142),
            ('1,2,3', 261214),
            ('2,3,1', 6895259),
            ('3,2,1', 18),
            ('3,1,2', 362),
        ]
        for t, r in tests:
            m = Memory(t)
            self.assertEqual(m.get(30000000), r)



#unittest.main()
m = Memory('14,8,16,0,1,17')
print(m.get(2020))
print(m.get(30000000))
