import unittest

class Bags:
    def __init__(self, rules):
        self.rules = {}
        for r in rules:
            color, l = self.parse_rule(r)
            self.rules[color] = l

    def parse_rule(self, rule):
        x, y = rule.split(' contain ')
        color = x[:-5]
        y = y[:-1]
        if y == 'no other bags':
            return color, []
        z = y.split(', ')
        l = []
        for e in z:
            if e[-5:] == ' bags':
                e = e[:-5]
            else:
                e = e[:-4]
            a, b = e.split(' ', 1)
            l.append((int(a), b))
        return color, l

    def find(self, cur, what):
        if cur == what:
            return True
        if cur not in self.rules:
            return False
        for _, n in self.rules[cur]:
            if self.find(n, what):
                return True
        return False

    def find_inside(self, cur):
        if cur not in self.rules:
            return 1
        res = 1
        for c, n in self.rules[cur]:
            res += c * self.find_inside(n)
        return res

    def find_all(self, what):
        res = []
        for col, _ in self.rules.items():
            if col == what:
                continue
            if self.find(col, what):
                res.append(col)
        return res


class TestBags(unittest.TestCase):
    def test_parse_rule(self):
        tests = [
            ('light red bags contain 1 bright white bag, 2 muted yellow bags.', 'light red', [(1, 'bright white'), (2, 'muted yellow')]),
            ('dark orange bags contain 3 bright white bags, 4 muted yellow bags.', 'dark orange', [(3, 'bright white'), (4, 'muted yellow')]),
            ('bright white bags contain 1 shiny gold bag.', 'bright white', [(1, 'shiny gold')]),
            ('muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.', 'muted yellow', [(2, 'shiny gold'), (9, 'faded blue')]),
            ('shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.', 'shiny gold', [(1, 'dark olive'), (2, 'vibrant plum')]),
            ('dark olive bags contain 3 faded blue bags, 4 dotted black bags.', 'dark olive', [(3, 'faded blue'), (4, 'dotted black')]),
            ('vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.', 'vibrant plum', [(5, 'faded blue'), (6, 'dotted black')]),
            ('faded blue bags contain no other bags.', 'faded blue', []),
            ('dotted black bags contain no other bags.', 'dotted black', []),
        ]
        for t, col, l in tests:
            b = Bags([])
            self.assertEqual(b.parse_rule(t), (col, l))

    def test_find(self):
        rules = [
            'light red bags contain 1 bright white bag, 2 muted yellow bags.',
            'dark orange bags contain 3 bright white bags, 4 muted yellow bags.',
            'bright white bags contain 1 shiny gold bag.',
            'muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.',
            'shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.',
            'dark olive bags contain 3 faded blue bags, 4 dotted black bags.',
            'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
            'faded blue bags contain no other bags.',
            'dotted black bags contain no other bags.',
        ]
        b = Bags(rules)
        self.assertEqual(sorted(b.find_all('shiny gold')), sorted(['bright white', 'muted yellow', 'dark orange', 'light red']))

    def test_inside(self):
        rules = [
            'shiny gold bags contain 2 dark red bags.',
            'dark red bags contain 2 dark orange bags.',
            'dark orange bags contain 2 dark yellow bags.',
            'dark yellow bags contain 2 dark green bags.',
            'dark green bags contain 2 dark blue bags.',
            'dark blue bags contain 2 dark violet bags.',
            'dark violet bags contain no other bags.',
        ]
        b = Bags(rules)
        self.assertEqual(b.find_inside('shiny gold'), 127)


#unittest.main()

l = []
while True:
    try:
        s = input()
    except:
        break
    l.append(s)
b = Bags(l)
print(len(b.find_all('shiny gold')))
print(b.find_inside('shiny gold') - 1)
