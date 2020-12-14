import unittest

class Masks:
    def __init__(self, c):
        self.c = c
        self.mem = {}
        self.mask = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    def cmd(self, c):
        a, b = c.split(' = ')
        if a == 'mask':
            self.mask = b
        elif a[:3] == 'mem':
            addr = int(a[4:-1])
            val = int(b)
            mul = 1
            res = 0
            for m in self.mask[::-1]:
                bit = val % 2
                if m == 'X':
                    res += mul * bit
                elif m == '1':
                    res += mul
                elif m == '0':
                    pass
                mul *= 2
                val //= 2
            self.mem[addr] = res

    def expand(self, a, i):
        if i == len(self.mask):
            return [a]
        b = 2 ** i
        c = self.mask[-1 - i]
        if c == '0':
            return self.expand(a, i + 1)
        elif c == '1':
            if (a // b) % 2 == 0:
                a += b
            return self.expand(a, i + 1)
        else:
            if (a // b) % 2 == 1:
                a -= b
            return self.expand(a, i + 1) + self.expand(a + b, i + 1)

    def cmd2(self, c):
        a, b = c.split(' = ')
        if a == 'mask':
            self.mask = b
        elif a[:3] == 'mem':
            addr = int(a[4:-1])
            val = int(b)
            l = self.expand(addr, 0)
            for m in l:
              self.mem[m] = val

    def get(self):
        for c in self.c:
            self.cmd(c)
        res = 0
        for k, v in self.mem.items():
            res += v
        return res

    def get2(self):
        for c in self.c:
            self.cmd2(c)
        res = 0
        for k, v in self.mem.items():
            res += v
        return res


class TestMasks(unittest.TestCase):
    def test_get(self):
        t = ['mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X', 'mem[8] = 11', 'mem[7] = 101', 'mem[8] = 0']
        m = Masks(t)
        self.assertEqual(m.get(), 165)

    def test_get2(self):
        t = ['mask = 000000000000000000000000000000X1001X', 'mem[42] = 100', 'mask = 00000000000000000000000000000000X0XX', 'mem[26] = 1']
        m = Masks(t)
        self.assertEqual(m.get2(), 208)


#unittest.main()

c = []
while True:
    try:
        l = input()
    except:
        break
    c.append(l)

m = Masks(c)
print(m.get2())
