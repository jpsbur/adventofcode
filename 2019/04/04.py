import unittest


class Password:

    def valid(self, x):
        x = int(x)
        if x < 0:
            return False
        s = str(x)
        if len(s) != 6:
            return False
        for i in range(5):
            if int(s[i]) > int(s[i + 1]):
                return False
        for i in range(5):
            if s[i] == s[i + 1]:
                return True
        return False

    def valid2(self, x):
        x = int(x)
        if x < 0:
            return False
        s = str(x)
        if len(s) != 6:
            return False
        for i in range(5):
            if int(s[i]) > int(s[i + 1]):
                return False
        for i in range(5):
            if s[i] == s[i + 1] and (i == 0 or s[i - 1] != s[i]) and (i == 4 or s[i + 2] != s[i]):
                return True
        return False


class TestPassword(unittest.TestCase):

    def test_valid(self):
        p = Password()
        self.assertTrue(p.valid(111111))
        self.assertFalse(p.valid(223450))
        self.assertFalse(p.valid(123789))
        self.assertFalse(p.valid(1))

    def test_valid2(self):
        p = Password()
        self.assertTrue(p.valid2(112233))
        self.assertFalse(p.valid2(123444))
        self.assertTrue(p.valid2(111122))
        self.assertFalse(p.valid2(1))


#unittest.main()

p = Password()
cnt = 0
for a in range(125730, 579382):
    if p.valid2(a):
        cnt += 1
print(cnt)
