import unittest

class Tickets:
    def __init__(self, rules):
        self.r = {}
        self.bad = {}
        for r in rules:
            n, x = r.split(': ')
            i = [tuple(map(int, y.split('-'))) for y in x.split(' or ')]
            self.r[n] = i
            self.bad[n] = {}

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

    def add_ticket(self, ticket):
        t = list(map(int, ticket.split(',')))
        for i in range(len(t)):
            x = t[i]
            for n, y in self.r.items():
                ok = False
                for (l, r) in y:
                    if l <= x <= r:
                        ok = True
                if not ok:
                    self.bad[n][i] = True

    def get_match(self):
        m = {}
        for n, b in self.bad.items():
            m[n] = []
            for i in range(len(self.bad.items())):
                if i not in b:
                    m[n].append(i)
        go = True
        while go:
            go = False
            for n, x in m.items():
                if len(x) > 1:
                    go = True
                    continue
                for n2, x2 in m.items():
                    if n2 == n:
                        continue
                    for i in range(len(x2)):
                        if x2[i] == x[0]:
                            m[n2] = m[n2][:i] + m[n2][i + 1:]
                            break
        return m


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

    def test_match(self):
        t = Tickets([
            'class: 0-1 or 4-19',
            'row: 0-5 or 8-19',
            'seat: 0-13 or 16-19',
        ])
        good = [
            '11,12,13',
            '3,9,18',
            '15,1,5',
            '5,14,9',
        ]
        for g in good:
            t.add_ticket(g)
        self.assertEqual(t.get_match(), {'class': [1], 'row': [0], 'seat': [2]})


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
    if len(f) == 0:
        good.append(l)
print(res)

for g in good:
    t.add_ticket(g)
match = t.get_match()
print(match)
res = 1
yourx = list(map(int, your.split(',')))
for n, ii in match.items():
    if n[:10] != 'departure ':
        continue
    res *= yourx[ii[0]]
print(res)
