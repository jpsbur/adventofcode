import unittest

class Ship():
    def __init__(self):
        self.x, self.y = 0, 0
        self.dx, self.dy = 1, 0

    def move(self, cmd):
        c = cmd[0]
        d = int(cmd[1:])
        if c == 'N':
            self.y += d
        elif c == 'S':
            self.y -= d
        elif c == 'E':
            self.x += d
        elif c == 'W':
            self.x -= d
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
            ('F10', (10, 0, 1, 0)),
            ('N3', (10, 3, 1, 0)),
            ('F7', (17, 3, 1, 0)),
            ('R90', (17, 3, 0, -1)),
            ('F11', (17, -8, 0, -1)),
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
