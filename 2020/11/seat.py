import unittest

class Seats:
    def __init__(self, a):
        self.a = [[y for y in x] for x in a]

    def cnt0(self, i, j):
        cnt = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if ni < 0 or ni >= len(self.a) or nj < 0 or nj >= len(self.a[i]):
                    continue
                if self.a[ni][nj] == '#':
                    cnt += 1
        return cnt

    def cnt1(self, i, j):
        cnt = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
                if di == 0 and dj == 0:
                    continue
                ni, nj = i, j
                while True:
                    ni += di
                    nj += dj
                    if ni < 0 or ni >= len(self.a) or nj < 0 or nj >= len(self.a[i]):
                        break
                    if self.a[ni][nj] != '.':
                        if self.a[ni][nj] == '#':
                            cnt += 1
                        break
        return cnt

    def iter(self, strategy=0):
        b = [[' ' for y in x] for x in self.a]
        change = False
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                b[i][j] = self.a[i][j]
                cnt = -1
                if strategy == 0:
                    cnt, threshold = self.cnt0(i, j), 4
                elif strategy == 1:
                    cnt, threshold = self.cnt1(i, j), 5
                if self.a[i][j] == 'L':
                    if cnt == 0:
                        b[i][j] = '#'
                        change = True
                elif self.a[i][j] == '#':
                    if cnt >= threshold:
                        b[i][j] = 'L'
                        change = True
        self.a = b
        return change

    def stable(self, strategy=0):
        while self.iter(strategy):
            pass

    def count(self):
        ans = 0
        for x in self.a:
            for y in x:
                if y == '#':
                    ans += 1
        return ans


class TestSeats(unittest.TestCase):
    def test_iter0(self):
        s = Seats([
            'L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL',
        ])
        s.iter()
        n = Seats([
            '#.##.##.##',
            '#######.##',
            '#.#.#..#..',
            '####.##.##',
            '#.##.##.##',
            '#.#####.##',
            '..#.#.....',
            '##########',
            '#.######.#',
            '#.#####.##',
        ])
        self.assertEqual(s.a, n.a)
        s.iter()
        n = Seats([
            '#.LL.L#.##',
            '#LLLLLL.L#',
            'L.L.L..L..',
            '#LLL.LL.L#',
            '#.LL.LL.LL',
            '#.LLLL#.##',
            '..L.L.....',
            '#LLLLLLLL#',
            '#.LLLLLL.L',
            '#.#LLLL.##',
        ])
        self.assertEqual(s.a, n.a)

    def test_iter1(self):
        s = Seats([
            'L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL',
        ])
        s.iter(1)
        n = Seats([
            '#.##.##.##',
            '#######.##',
            '#.#.#..#..',
            '####.##.##',
            '#.##.##.##',
            '#.#####.##',
            '..#.#.....',
            '##########',
            '#.######.#',
            '#.#####.##',
        ])
        self.assertEqual(s.a, n.a)
        s.iter(1)
        n = Seats([
            '#.LL.LL.L#',
            '#LLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLL#',
            '#.LLLLLL.L',
            '#.LLLLL.L#',
        ])
        self.assertEqual(s.a, n.a)

    def test_stable(self):
        s = Seats([
            'L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL',
        ])
        s.stable()
        n = Seats([
            '#.#L.L#.##',
            '#LLL#LL.L#',
            'L.#.L..#..',
            '#L##.##.L#',
            '#.#L.LL.LL',
            '#.#L#L#.##',
            '..L.L.....',
            '#L#L##L#L#',
            '#.LLLLLL.L',
            '#.#L#L#.##',
        ])
        self.assertEqual(s.a, n.a)
        self.assertEqual(s.count(), 37)

        s = Seats([
            'L.LL.LL.LL',
            'LLLLLLL.LL',
            'L.L.L..L..',
            'LLLL.LL.LL',
            'L.LL.LL.LL',
            'L.LLLLL.LL',
            '..L.L.....',
            'LLLLLLLLLL',
            'L.LLLLLL.L',
            'L.LLLLL.LL',
        ])
        s.stable(1)
        n = Seats([
            '#.L#.L#.L#',
            '#LLLLLL.LL',
            'L.L.L..#..',
            '##L#.#L.L#',
            'L.L#.LL.L#',
            '#.LLLL#.LL',
            '..#.L.....',
            'LLL###LLL#',
            '#.LLLLL#.L',
            '#.L#LL#.L#',
        ])
        self.assertEqual(s.a, n.a)
        self.assertEqual(s.count(), 26)


#unittest.main()

l = []
while True:
    try:
        s = input()
    except:
        break
    l.append(s)
s = Seats(l)
s.stable(1)
print(s.a)
print(s.count())
