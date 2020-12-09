import unittest

class Form:
    def __init__(self, e):
        self.e = e

    def get_all(self):
        res = {}
        for x in self.e:
            for c in x:
                res[c] = True
        return len(res)

    def get_every(self):
        res = {}

        for x in self.e:
            for c in x:
                if c not in res:
                    res[c] = 0
                res[c] += 1

        ans = 0
        for k, v in res.items():
            if v == len(self.e):
                ans += 1
        return ans


class TestForm(unittest.TestCase):
    def test_get_all(self):
        tests = [
            (['abc'], 3),
            (['a', 'b', 'c'], 3),
            (['ab', 'ac'], 3),
            (['a', 'a', 'a', 'a'], 1),
            (['b'], 1),
        ]
        for inp, exp in tests:
            f = Form(inp)
            self.assertEqual(f.get_all(), exp)

    def test_get_every(self):
        tests = [
            (['abc'], 3),
            (['a', 'b', 'c'], 0),
            (['ab', 'ac'], 1),
            (['a', 'a', 'a', 'a'], 1),
            (['b'], 1),
        ]
        for inp, exp in tests:
            f = Form(inp)
            self.assertEqual(f.get_every(), exp)


#unittest.main()

inp = []
while True:
    cur = []
    while True:
        try:
            l = input()
        except:
            break
        if len(l) == 0:
            break
        cur.append(l)
    if len(cur) == 0:
        break
    inp.append(cur)

ans = 0
for t in inp:
    f = Form(t)
    ans += f.get_every()

print(ans)
