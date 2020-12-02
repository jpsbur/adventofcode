import unittest

class Password:

    def verify1(self, c, cmin, cmax, p):
        """Verify that p contains at least cmin and at most cmax occurrences of c."""
        cnt = 0
        for cur in p:
            if cur == c:
                cnt += 1
        return cmin <= cnt <= cmax

    def verify2(self, c, p1, p2, p):
        """Verfy that exactly one of p1/p2 positions (1-based) in p contains character c."""
        cnt = 0
        if p[p1 - 1] == c:
            cnt += 1
        if p[p2 - 1] == c:
            cnt += 1
        return cnt == 1


class TestPassword(unittest.TestCase):

    def test_verify1(self):
        tests = [
          ('a', 1, 3, 'abcde', True),
          ('b', 1, 3, 'cdefg', False),
          ('c', 2, 9, 'ccccccccc', True),
        ]
        e = Password()
        for test in tests:
            c, cmin, cmax, p, exp = test
            self.assertEqual(e.verify1(c, cmin, cmax, p), exp)

    def test_verify2(self):
        tests = [
          ('a', 1, 3, 'abcde', True),
          ('b', 1, 3, 'cdefg', False),
          ('c', 2, 9, 'ccccccccc', False),
        ]
        e = Password()
        for test in tests:
            c, p1, p2, p, exp = test
            self.assertEqual(e.verify2(c, p1, p2, p), exp)


#unittest.main()

l = []
while True:
    try:
        x = input()
        l.append(x)
    except:
        break

e = Password()
cnt = 0
for t in l:
    [r, c, p] = t.split()
    [cmin, cmax] = list(map(int, r.split('-')))
    if e.verify2(c[0], cmin, cmax, p):
        cnt += 1
print(cnt)
