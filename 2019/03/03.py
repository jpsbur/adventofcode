import unittest

class Wires:

    def get_earliest_intersection(self, a_, b_):
        a = self.get_points(a_)
        b = self.get_points(b_)
        best = None
        alen = 0
        for i in range(1, len(a)):
            blen = 0
            for j in range(1, len(b)):
                x = self.intersect2((a[i - 1], a[i]), (b[j - 1], b[j]))
                if x:
                    res = alen + self.dist(a[i - 1], x) + blen + self.dist(b[j - 1], x)
                    if not best or best > res:
                        best = res
                blen += self.dist(b[j - 1], b[j])
            alen += self.dist(a[i - 1], a[i])
        return best

    def dist(self, a, b):
        xa, ya = a
        xb, yb = b
        return abs(xa - xb) + abs(ya - yb)

    def get_intersection(self, a_, b_):
        a = self.get_points(a_)
        b = self.get_points(b_)
        best = None
        for i in range(1, len(a)):
            for j in range(1, len(b)):
                x = self.intersect((a[i - 1], a[i]), (b[j - 1], b[j]))
                if x and (not best or x < best):
                    best = x
        return best

    def intersect(self, a, b):
        ((xa1, ya1), (xa2, ya2)) = a
        ((xb1, yb1), (xb2, yb2)) = b
        xmin = max(min(xa1, xa2), min(xb1, xb2))
        xmax = min(max(xa1, xa2), max(xb1, xb2))
        ymin = max(min(ya1, ya2), min(yb1, yb2))
        ymax = min(max(ya1, ya2), max(yb1, yb2))
        if xmin <= xmax and ymin <= ymax:
            return abs(xmin) + abs(ymin)
        return None

    def intersect2(self, a, b):
        ((xa1, ya1), (xa2, ya2)) = a
        ((xb1, yb1), (xb2, yb2)) = b
        xmin = max(min(xa1, xa2), min(xb1, xb2))
        xmax = min(max(xa1, xa2), max(xb1, xb2))
        ymin = max(min(ya1, ya2), min(yb1, yb2))
        ymax = min(max(ya1, ya2), max(yb1, yb2))
        if xmin <= xmax and ymin <= ymax:
            return (xmin, ymin)
        return None

    def get_points(self, a_):
        a = a_.split(',')
        x, y = 0, 0
        res = [(x, y)]
        for p in a:
            c = p[0]
            d = int(p[1:])
            if c == 'U':
                y += d
            elif c == 'D':
                y -= d
            elif c == 'R':
                x += d
            elif c == 'L':
                x -= d
            else:
                raise Exception()
            res.append((x, y))
        return res


class TestWires(unittest.TestCase):

    def test_get_points(self):
        w = Wires()
        self.assertEqual([(0, 0), (75, 0), (75, -30), (158, -30), (158, 53), (146, 53), (146, 4), (217, 4), (217, 11), (145, 11)],
            w.get_points("R75,D30,R83,U83,L12,D49,R71,U7,L72"))

    def test_get_intersection(self):
        w = Wires()
        self.assertEqual(159, w.get_intersection("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"))
        self.assertEqual(135, w.get_intersection("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))

    def test_get_earliest_intersection(self):
        w = Wires()
        self.assertEqual(610, w.get_earliest_intersection("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"))
        self.assertEqual(410, w.get_earliest_intersection("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"))



#unittest.main()

wires = Wires()
a = input()
b = input()
print(wires.get_earliest_intersection(a, b))
