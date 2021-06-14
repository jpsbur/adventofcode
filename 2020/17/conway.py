import unittest

class ConwayCubes:
    def __init__(self, a, d):
        self.d = len(a) + d * 2
        self.h = len(a[0]) + d * 2
        self.w = len(a[0][0]) + d * 2
        self.a = [[['.'] * self.w] * self.h] * self.d
        for i in range(len(a)):
            for j in range(len(a[i])):
                for k in range(len(a[i][j])):
                    print(a[i][j][k])
                    self.a[i + d][j + d][k + d] = a[i][j][k]
    
    def iter(self):
        na = [[['.'] * self.w] * self.h] * self.d
        for i in range(self.d):
            for j in range(self.h):
                for k in range(self.w):
                    c = self.get_neighbors(i, j, k)
                    n = self.a[i][j][k]
                    if n == '#':
                        if c not in [2, 3]:
                            n = '.'
                    else:
                        if c == 3:
                            n = '#'
                    na[i][j][k] = n
        self.a = na

    def get_neighbors(self, i, j, k):
        res = 0
        for di in range(-1, 2):
            for dj in range(-1, 2):
                for dk in range(-1, 2):
                    if di == 0 and dj == 0 and dk == 0:
                        continue
                    ni, nj, nk = i + di, j + dj, k + dk
                    if not (0 <= ni < self.d and 0 <= nj < self.h and 0 <= nk < self.w):
                        continue
                    if self.a[ni][nj][nk] == '#':
                        res += 1
        return res


class TestConwayCubes(unittest.TestCase):
    def test_iter(self):
        c = ConwayCubes([[
            '.#.',
            '..#',
            '###',
        ]], 2)
        c.iter()
        nc = ConwayCubes([
            [
                '.......',
                '.......',
                '.......',
                '.......',
                '.......',
                '.......',
                '.......',
            ],
            [
                '.......',
                '.......',
                '..#....',
                '....#..',
                '...#...',
                '.......',
                '.......',
            ],
            [
                '.......',
                '.......',
                '..#.#..',
                '...##..',
                '...#...',
                '.......',
                '.......',
            ],
            [
                '.......',
                '.......',
                '..#....',
                '....#..',
                '...#...',
                '.......',
                '.......',
            ],
            [
                '.......',
                '.......',
                '.......',
                '.......',
                '.......',
                '.......',
                '.......',
            ],
        ], 0)
        self.assertEqual(c.a, nc.a)
        c.iter()
        nc = ConwayCubes([
            [
                '.......',
                '.......',
                '.......',
                '...#...',
                '.......',
                '.......',
                '.......',
            ],
            [
                '.......',
                '...#...',
                '..#..#.',
                '.....#.',
                '..#....',
                '.......',
                '.......',
            ],
            [
                '.......',
                '.##....',
                '.##....',
                '.#.....',
                '.....#.',
                '..###..',
                '.......',
            ],
            [
                '.......',
                '...#...',
                '..#..#.',
                '.....#.',
                '..#....',
                '.......',
                '.......',
            ],
            [
                '.......',
                '.......',
                '.......',
                '...#...',
                '.......',
                '.......',
                '.......',
            ],
        ], 0)
        self.assertEqual(c.a, nc.a)


#unittest.main()

a = []
while True:
    try:
        l = input()
    except:
        break
    a.append(l)

print([a])

n = 6
c = ConwayCubes([a], n)
for i in range(n):
    ans = 0
    for x in c.a:
        for y in x:
            for z in y:
                if z == '#':
                    ans += 1
    print(ans)
    c.iter()
