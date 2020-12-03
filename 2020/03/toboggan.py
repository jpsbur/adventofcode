import unittest

class Toboggan:

    def __init__(self, m):
        self.m = m
        self.h = len(m)
        self.w = len(m[0])

    def count(self, d):
        dx, dy = d
        x, y = dx, dy
        cnt = 0
        while y < self.h:
            if self.m[y][x] == '#':
                cnt += 1
            x, y = (x + dx) % self.w, y + dy
        return cnt


class TestToboggan(unittest.TestCase):
    def test_count(self):
        t = Toboggan([
            '..##.......',
            '#...#...#..',
            '.#....#..#.',
            '..#.#...#.#',
            '.#...##..#.',
            '..#.##.....',
            '.#.#.#....#',
            '.#........#',
            '#.##...#...',
            '#...##....#',
            '.#..#...#.#',
            ])
        self.assertEqual(t.count((1, 1)), 2)
        self.assertEqual(t.count((3, 1)), 7)
        self.assertEqual(t.count((5, 1)), 3)
        self.assertEqual(t.count((7, 1)), 4)
        self.assertEqual(t.count((1, 2)), 2)


#unittest.main()

m = []
while True:
    try:
        l = input()
    except:
        break
    m.append(l)
t = Toboggan(m)
ans = 1
for d in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    x = t.count(d)
    ans *= x
print(ans)
