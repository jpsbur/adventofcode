import unittest


class ImageDecoder:
    
    def __init__(self, w, h, a):
        self.w, self.h = w, h
        n = len(a) // (w * h)
        assert n * w * h == len(a)
        self.layers = []
        for i in range(n):
            st = i * w * h
            l = [[a[st + j * w + k] for k in range(w)] for j in range(h)]
            self.layers.append(l)

    def get_checksum(self):
        best = None
        res = None
        for l in self.layers:
            c = {'0': 0, '1': 0, '2': 0}
            for a in l:
                for b in a:
                    if b not in c:
                        c[b] = 0
                    c[b] += 1
            if best is None or c['0'] < best:
                best = c['0']
                res = c['1'] * c['2']
        return res

    def get_stacked(self):
        res = self.layers[-1]
        for i in range(self.h):
            for j in range(self.w):
                l = 0
                while l < len(self.layers) and self.layers[l][i][j] == '2':
                    l += 1
                res[i][j] = self.layers[l][i][j]
        return res


class TestImageDecoder(unittest.TestCase):
    
    def test_image_decoder(self):
        d = ImageDecoder(3, 2, "123456789012")
        self.assertEqual([[['1', '2', '3'], ['4', '5', '6']], [['7', '8', '9'], ['0', '1', '2']]], d.layers)

    def test_checksum(self):
        d = ImageDecoder(3, 2, "123456789012")
        self.assertEqual(1, d.get_checksum())

    def test_stacked(self):
        d = ImageDecoder(2, 2, "0222112222120000")
        self.assertEqual([['0', '1'], ['1', '0']], d.get_stacked())


#unittest.main()

d = ImageDecoder(25, 6, input())
print(d.get_checksum())
x = d.get_stacked()
for a in x:
    print(''.join(['*' if b == '1' else ' ' for b in a]))
