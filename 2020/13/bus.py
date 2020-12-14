import unittest

class Bus:
    def __init__(self, conf):
        self.buses = list(conf.split(','))

    def get_earliest(self, t):
        min_wait = 1e100
        min_bus = -1
        for x in self.buses:
            if x == 'x':
                continue
            d = int(x)
            wait = (d - (t % d)) % d
            if wait < min_wait:
                min_wait, min_bus = wait, d
        return min_wait, min_bus

    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a % b)

    def lcm(self, a, b):
        return a * b // self.gcd(a, b)

    def get_seq(self):
        t = 0
        l = 1
        for i in range(len(self.buses)):
            if self.buses[i] == 'x':
                continue
            d = int(self.buses[i])
            while (t + i) % d != 0:
                t += l
            l = self.lcm(l, d)
        return t


class TestBus(unittest.TestCase):
    def test_get_earliest(self):
        b = Bus('7,13,x,x,59,x,31,19')
        self.assertEqual(b.get_earliest(939), (5, 59))

    def test_seq(self):
        tests = [
          ('17,x,13,19', 3417),
          ('67,7,59,61', 754018),
          ('67,x,7,59,61', 779210),
          ('67,7,x,59,61', 1261476),
          ('1789,37,47,1889', 1202161486),
          ('7,13,x,x,59,x,31,19', 1068781),
        ]
        for conf, exp in tests:
            b = Bus(conf)
            self.assertEqual(b.get_seq(), exp)


#unittest.main()

t = int(input())
c = input()
b = Bus(c)
wait, bus = b.get_earliest(t)
print(wait, bus, wait * bus)
print(b.get_seq())
