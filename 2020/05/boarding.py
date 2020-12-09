import unittest
import logging

class BoardingPass:
    def __init__(self, num):
        self.num = num

    def row(self):
        r = self.num[:7]
        res = 0
        for c in r:
            res *= 2
            if c == 'B':
                res += 1
        return res

    def column(self):
        r = self.num[7:]
        res = 0
        for c in r:
            res *= 2
            if c == 'R':
                res += 1
        return res

    def seat_id(self):
        return self.row() * 8 + self.column()


class TestBoardingPass(unittest.TestCase):
    def test_seat_id(self):
        tests = [
            ('FBFBBFFRLR', 44, 5, 357),
            ('BFFFBBFRRR', 70, 7, 567),
            ('FFFBBBFRRR', 14, 7, 119),
            ('BBFFBBFRLL', 102, 4, 820),
        ]
        for t in tests:
            num, row, column, seat_id = t
            p = BoardingPass(num)
            self.assertEqual(p.row(), row)
            self.assertEqual(p.column(), column)
            self.assertEqual(p.seat_id(), seat_id)


#unittest.main()

res = -1
l = []
while True:
    try:
        s = input()
    except:
        break
    b = BoardingPass(s)
    s = b.seat_id()
    l.append(s)
    if s > res:
        res = s

print(res)

l.sort()
ans = -1
for i in range(len(l) - 1):
    if l[i + 1] == l[i] + 2:
        ans = l[i] + 1
        break
print(ans)
