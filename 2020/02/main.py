import unittest

class Password:

    def verify(self, c, cmin, cmax, p):
        """Verify that p contains at least cmin and at most cmax occurrences of c."""
        cnt = 0
        for cur in p:
            if cur == c:
                cnt += 1
        return cmin <= cnt <= cmax


class TestPassword(unittest.TestCase):

    def test_verify(self):
        tests = [
          ('a', 1, 3, 'abcde', True),
          ('b', 1, 3, 'cdefg', False),
          ('c', 2, 9, 'ccccccccc', True),
        ]
        e = Password()
        for test in tests:
            c, cmin, cmax, p, exp = test
            self.assertEqual(e.verify(c, cmin, cmax, p), exp)


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
    if e.verify(c[0], cmin, cmax, p):
        cnt += 1
print(cnt)
