import unittest

class Orbit:

    def __init__(self, o):
        self.to = {}
        self.p = {}
        self.v = {}
        for x in o:
            [a, b] = x.split(')')
            self.v[a] = True
            self.v[b] = True
            if a not in self.to:
                self.to[a] = []
            self.to[a].append(b)
            self.p[b] = a

    def total_orbits(self):
        ans = 0
        for a in self.p.keys():
            x = a
            while x in self.p:
                ans += 1
                x = self.p[x]
        return ans

    def dist(self, a, b):
        vis = {}
        d = {}
        d[a] = 0
        q = [a]
        i = 0
        while i < len(q):
            x = q[i]
            i += 1
            to = []
            if x in self.to:
                to = self.to[x]
            if x in self.p:
                to.append(self.p[x])
            for y in to:
                if y not in vis:
                    d[y] = d[x] + 1
                    q.append(y)
                    vis[y] = True
        return d[b]


class TestOrbitIntcode(unittest.TestCase):

    def test_next_step(self):
        f = Orbit(["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L"])
        self.assertEqual(42, f.total_orbits())

    def test_dist(self):
        f = Orbit(["COM)B", "B)C", "C)D", "D)E", "E)F", "B)G", "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN"])
        self.assertEqual(6, f.dist("YOU", "SAN"))


#unittest.main()

o = []
while True:
    try:
        s = input()
    except:
        break
    o.append(s)
orbit = Orbit(o)
print(orbit.total_orbits())
print(orbit.dist("YOU", "SAN") - 2)
