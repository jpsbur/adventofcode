import unittest

class Tickets:
    def __init__(self, rules):
        self.r = {}
        for r in rules:
            n, x = r.split(': ')
            i = [tuple(map(int, y.split('-'))) for y in x.split(' or ')]
            self.r[n] = i

    def match_any(self, x):
        for _, i in self.r.items():
            for (l, r) in i:
                if l <= x <= r:
                    return True
        return False

    def invalid_fields(self, ticket):
        t = list(map(int, ticket.split(',')))
        res = []
        for x in t:
            if not self.match_any(x):
                res.append(x)
        return res


class TestTickets(unittest.TestCase):
    def test_invalid_fields(self):
        t = Tickets([
            'class: 1-3 or 5-7',
            'row: 6-11 or 33-44',
            'seat: 13-40 or 45-50',
        ])
        tests = [
            ('7,3,47', []),
            ('40,4,50', [4]),
            ('55,2,20', [55]),
            ('38,6,12', [12]),
        ]
        for test, exp in tests:
            self.assertEqual(t.invalid_fields(test), exp)


#unittest.main()

r = []
while True:
    l = input()
    if l == '':
        break
    r.append(l)
t = Tickets(r)

print(input())
your = input()

input()
print(input())
res = 0
good = [your]
while True:
    try:
        l = input()
    except:
        break
    f = t.invalid_fields(l)
    print(f)
    for x in f:
        res += x
    if len(x) == 0:
        good.append(x)
print(res)


