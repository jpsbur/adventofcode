import unittest

class Ship():
    def __init__(self):
        self.x, self.y = 0, 0
        self.dx, self.dy = 10, 1

    def move(self, cmd):
        c = cmd[0]
        d = int(cmd[1:])
        if c == 'N':
            self.dy += d
        elif c == 'S':
            self.dy -= d
        elif c == 'E':
            self.dx += d
        elif c == 'W':
            self.dx -= d
        elif c == 'F':
            self.x += d * self.dx
            self.y += d * self.dy
        elif c in 'LR':
            if c == 'R':
                d = -d
            d = ((d % 360) + 360) % 360
            if d == 0:
                pass
            elif d == 90:
                self.dx, self.dy = -self.dy, self.dx
            elif d == 180:
                self.dx, self.dy = -self.dx, -self.dy
            elif d == 270:
                self.dx, self.dy = self.dy, -self.dx
            else:
                assert False
        else:
            assert False

    def get(self):
        return abs(self.x) + abs(self.y)


class TestShip(unittest.TestCase):
    def test_move(self):
        s = Ship()
        tests = [
            ('F10', (100, 10, 10, 1)),
            ('N3', (100, 10, 10, 4)),
            ('F7', (170, 38, 10, 4)),
            ('R90', (170, 38, 4, -10)),
            ('F11', (214, -72, 4, -10)),
        ]
        for m, p in tests:
            s.move(m)
            self.assertEqual((s.x, s.y, s.dx, s.dy), p)


#unittest.main()

s = Ship()
while True:
    try:
        l = input()
    except:
        break
    s.move(l)
print(s.get())
