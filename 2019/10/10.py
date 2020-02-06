import unittest
import math
import functools


class Vec:
    
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def sub(self, other):
        return Vec(self.x - other.x, self.y - other.y)

    def add(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def norm(self):
        d = math.gcd(abs(self.x), abs(self.y))
        if d == 0:
            d = 1
        return Vec(self.x // d, self.y // d)


class Map:
    
    def __init__(self, a):
        self.a = [list(x) for x in a]
        self.h = len(a)
        self.w = len(a[0])

    def get_point(self, a):
        return self.a[a.y][a.x]

    def set_point(self, a, val):
        self.a[a.y][a.x] = val

    def is_visible(self, a, b):
        if a == b:
            return False
        d = b.sub(a).norm()
        x = a.add(d)
        while x != b:
            if self.get_point(x) != '.':
                return False
            x = x.add(d)
        return True

    def all_asteroids(self):
        for y in range(self.h):
            for x in range(self.w):
                b = Vec(x, y)
                if self.get_point(b) == '#':
                    yield b

    def all_visible(self, a):
        for b in self.all_asteroids():
            if self.is_visible(a, b):
                yield b

    def count_visible(self, a):
        cnt = 0
        for b in self.all_visible(a):
            cnt += 1
        return cnt

    def max_visible(self):
        best = 0
        best_point = None
        for b in self.all_asteroids():
            cnt = self.count_visible(b)
            if cnt > best:
                best, best_point = cnt, b
        return best, best_point

    def destroy_order(self, a):
        while True:
            batch = list(self.all_visible(a))
            if len(batch) == 0:
                break
            right = []
            left = []
            for b in batch:
                z = b.sub(a)
                if z.x > 0 or z.x == 0 and z.y < 0:
                    right.append(b)
                else:
                    left.append(b)
            comparator = lambda v, u: u.sub(a).cross(v.sub(a))
            right.sort(key=functools.cmp_to_key(comparator))
            left.sort(key=functools.cmp_to_key(comparator))
            for b in right + left:
                yield b
                self.set_point(b, '.')


class TestMap(unittest.TestCase):

    def test_destroy_order(self):
        m = Map([
            ".#....#####...#..",
            "##...##.#####..##",
            "##...#...#.#####.",
            "..#.....X...###..",
            "..#.#.....#....##",
        ])
        self.assertEqual([
            Vec(8, 1), Vec(9, 0), Vec(9, 1), Vec(10, 0), Vec(9, 2), Vec(11, 1), Vec(12, 1), Vec(11, 2), Vec(15, 1),
            Vec(12, 2), Vec(13, 2), Vec(14, 2), Vec(15, 2), Vec(12, 3), Vec(16, 4), Vec(15, 4), Vec(10, 4), Vec(4, 4),
            Vec(2, 4), Vec(2, 3), Vec(0, 2), Vec(1, 2), Vec(0, 1), Vec(1, 1), Vec(5, 2), Vec(1, 0), Vec(5, 1),
            Vec(6, 1), Vec(6, 0), Vec(7, 0), Vec(8, 0), Vec(10, 1), Vec(14, 0), Vec(16, 1), Vec(13, 3), Vec(14, 3),
            ], list(m.destroy_order(Vec(8, 3))))

    def test_max_visible(self):
        m = Map([
            "......#.#.",
            "#..#.#....",
            "..#######.",
            ".#.#.###..",
            ".#..#.....",
            "..#....#.#",
            "#..#....#.",
            ".##.#..###",
            "##...#..#.",
            ".#....####",
        ])
        self.assertEqual((33, Vec(5, 8)), m.max_visible())
        m = Map([
            "#.#...#.#.",
            ".###....#.",
            ".#....#...",
            "##.#.#.#.#",
            "....#.#.#.",
            ".##..###.#",
            "..#...##..",
            "..##....##",
            "......#...",
            ".####.###.",
        ])
        self.assertEqual((35, Vec(1, 2)), m.max_visible())
        m = Map([
            ".#..#..###",
            "####.###.#",
            "....###.#.",
            "..###.##.#",
            "##.##.#.#.",
            "....###..#",
            "..#.#..#.#",
            "#..#.#.###",
            ".##...##.#",
            ".....#.#..",
        ])
        self.assertEqual((41, Vec(6, 3)), m.max_visible())
        m = Map([
            ".#..##.###...#######",
            "##.############..##.",
            ".#.######.########.#",
            ".###.#######.####.#.",
            "#####.##.#.##.###.##",
            "..#####..#.#########",
            "####################",
            "#.####....###.#.#.##",
            "##.#################",
            "#####.##.###..####..",
            "..######..##.#######",
            "####.##.####...##..#",
            ".#####..#.######.###",
            "##...#.##########...",
            "#.##########.#######",
            ".####.#.###.###.#.##",
            "....##.##.###..#####",
            ".#.#.###########.###",
            "#.#.#.#####.####.###",
            "###.##.####.##.#..##",
        ])
        self.assertEqual((210, Vec(11, 13)), m.max_visible())

    def test_count_visible(self):
        m = Map([
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"])
        self.assertEqual(7, m.count_visible(Vec(1, 0)))
        self.assertEqual(7, m.count_visible(Vec(4, 0)))
        self.assertEqual(6, m.count_visible(Vec(0, 2)))
        self.assertEqual(7, m.count_visible(Vec(1, 2)))
        self.assertEqual(7, m.count_visible(Vec(2, 2)))
        self.assertEqual(7, m.count_visible(Vec(3, 2)))
        self.assertEqual(5, m.count_visible(Vec(4, 2)))
        self.assertEqual(7, m.count_visible(Vec(4, 3)))
        self.assertEqual(8, m.count_visible(Vec(3, 4)))
        self.assertEqual(7, m.count_visible(Vec(4, 4)))
    
    def test_is_visible(self):
        m = Map([
            ".#..#",
            ".....",
            "#####",
            "....#",
            "...##"])
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(0, 2)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(1, 2)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(2, 2)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(3, 2)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(4, 2)))
        self.assertFalse(m.is_visible(Vec(3, 4), Vec(1, 0)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(4, 0)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(4, 3)))
        self.assertTrue(m.is_visible(Vec(3, 4), Vec(4, 4)))
        self.assertFalse(m.is_visible(Vec(3, 4), Vec(3, 4)))


#unittest.main()

m = Map([
    ".###..#######..####..##...#",
    "########.#.###...###.#....#",
    "###..#...#######...#..####.",
    ".##.#.....#....##.#.#.....#",
    "###.#######.###..##......#.",
    "#..###..###.##.#.#####....#",
    "#.##..###....#####...##.##.",
    "####.##..#...#####.#..###.#",
    "#..#....####.####.###.#.###",
    "#..#..#....###...#####..#..",
    "##...####.######....#.####.",
    "####.##...###.####..##....#",
    "#.#..#.###.#.##.####..#...#",
    "..##..##....#.#..##..#.#..#",
    "##.##.#..######.#..#..####.",
    "#.....#####.##........#####",
    "###.#.#######..#.#.##..#..#",
    "###...#..#.#..##.##..#####.",
    ".##.#..#...#####.###.##.##.",
    "...#.#.######.#####.#.####.",
    "#..##..###...###.#.#..#.#.#",
    ".#..#.#......#.###...###..#",
    "#.##.#.#..#.#......#..#..##",
    ".##.##.##.#...##.##.##.#..#",
    "#.###.#.#...##..#####.###.#",
    "#.####.#..#.#.##.######.#..",
    ".#.#####.##...#...#.##...#.",
])
res, b = m.max_visible()
print(res, b.x, b.y)
o = list(m.destroy_order(b))
print(o[200 - 1].x * 100 + o[200 - 1].y)
