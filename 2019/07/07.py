import unittest
import itertools

class Intcode:

    def get_op(self, code, i, j):
        op = code[i] // 100
        if (op // (10 ** j)) % 10 == 0:
            return code[code[i + 1 + j]]
        return code[i + 1 + j]

    def next_step(self, code_, i, fin_, fout_):
        code = code_[:]
        op = code[i]
        rop = op % 100
        if op == 99:
            return code, i, fin[:], fout[:]
        if rop == 1:
            a = self.get_op(code, i, 0)
            b = self.get_op(code, i, 1)
            code[code[i + 3]] = a + b
            fin, fout = fin_[:], fout_[:]
            i += 4
        elif rop == 2:
            a = self.get_op(code, i, 0)
            b = self.get_op(code, i, 1)
            code[code[i + 3]] = a * b
            fin, fout = fin_[:], fout_[:]
            i += 4
        elif rop == 3:
            code[code[i + 1]] = fin_[0]
            fin, fout = fin_[1:], fout_[:]
            i += 2
        elif rop == 4:
            if (op // 100) % 10 == 0:
                fin, fout = fin_[:], fout_[:] + [code[code[i + 1]]]
            else:
                fin, fout = fin_[:], fout_[:] + [code[i + 1]]
            i += 2
        elif rop == 5:
            a = self.get_op(code, i, 0)
            b = self.get_op(code, i, 1)
            if a != 0:
                i = b
            else:
                i += 3
            fin, fout = fin_, fout_
        elif rop == 6:
            a = self.get_op(code, i, 0)
            b = self.get_op(code, i, 1)
            if a == 0:
                i = b
            else:
                i += 3
            fin, fout = fin_, fout_
        elif rop == 7:
            a = self.get_op(code, i, 0)
            b = self.get_op(code, i, 1)
            if a < b:
                code[code[i + 3]] = 1
            else:
                code[code[i + 3]] = 0
            i += 4
            fin, fout = fin_, fout_
        elif rop == 8:
            a = self.get_op(code, i, 0)
            b = self.get_op(code, i, 1)
            if a == b:
                code[code[i + 3]] = 1
            else:
                code[code[i + 3]] = 0
            i += 4
            fin, fout = fin_, fout_
        return code, i, fin, fout

    def run(self, code_, fin_):
        code = code_[:]
        pos = 0
        fin = fin_
        fout = []
        while code[pos] != 99:
            code, pos, fin, fout = self.next_step(code, pos, fin, fout)
        return fout

    def max_phase(self, code_):
        best = -1
        for p in list(itertools.permutations(range(5))):
            x = 0
            for i in range(5):
                x = self.run(code_[:], [p[i], x])[0]
            if best is None or x > best:
                 best = x
        return best

    def run_parallel(self, codes_, inps_):
        codes = codes_[:]
        n = len(codes)
        stream = inps_[:]
        stream[0].append(0)
        pos = [0 for _ in range(n)]
        while True:
            any_step = False
            for i in range(n):
                if codes[i][pos[i]] == 99:
                    continue
                if codes[i][pos[i]] % 100 == 3 and len(stream[i]) == 0:
                    continue
                codes[i], pos[i], stream[i], stream[(i + 1) % n] = self.next_step(codes[i], pos[i], stream[i], stream[(i + 1) % n])
                any_step = True
                break
            if not any_step:
                break
        return stream[0]

    def max_phase_parallel(self, code):
        best = None
        for p in list(itertools.permutations([5, 6, 7, 8, 9])):
            x = self.run_parallel([code[:] for _ in range(5)], [[a] for a in p])[0]
            if best is None or x > best:
                best = x
        return best


class TestIntcode(unittest.TestCase):

    def test_max_phase_parallel(self):
        f = Intcode()
        code = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
        self.assertEqual(139629729, f.max_phase_parallel(code))
        code = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
        self.assertEqual(18216, f.max_phase_parallel(code))

    def test_run_parallel(self):
        f = Intcode()
        code = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
        self.assertEqual([139629729], f.run_parallel([code for _ in range(5)], [[9], [8], [7], [6], [5]]))
        code = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10]
        self.assertEqual([18216], f.run_parallel([code for _ in range(5)], [[9], [7], [8], [5], [6]]))

    def test_max_phase(self):
        f = Intcode()
        code = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
        self.assertEqual(43210, f.max_phase(code))
        code = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
        self.assertEqual(54321, f.max_phase(code))
        code = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
        self.assertEqual(65210, f.max_phase(code))

    def test_run_999(self):
        f = Intcode()
        code = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]
        fout = f.run(code, [-100])
        self.assertEqual(fout, [999])
        fout = f.run(code, [8])
        self.assertEqual(fout, [1000])
        fout = f.run(code, [99])
        self.assertEqual(fout, [1001])

    def test_run_jump(self):
        f = Intcode()
        fout = f.run([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0])
        self.assertEqual(fout, [0])
        fout = f.run([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [9])
        self.assertEqual(fout, [1])
        fout = f.run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0])
        self.assertEqual(fout, [0])
        fout = f.run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [-9])
        self.assertEqual(fout, [1])

    def test_run_lessi8(self):
        f = Intcode()
        fout = f.run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [7])
        self.assertEqual(fout, [1])
        fout = f.run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [8])
        self.assertEqual(fout, [0])
        fout = f.run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [7])
        self.assertEqual(fout, [1])
        fout = f.run([3, 3, 1107, -1, 8, 3, 4, 3, 99], [8])
        self.assertEqual(fout, [0])

    def test_run_eq8(self):
        f = Intcode()
        fout = f.run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8])
        self.assertEqual(fout, [1])
        fout = f.run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [13])
        self.assertEqual(fout, [0])
        fout = f.run([3, 3, 1108, -1, 8, 3, 4, 3, 99], [8])
        self.assertEqual(fout, [1])
        fout = f.run([3, 3, 1108, -1, 8, 3, 4, 3, 99], [13])
        self.assertEqual(fout, [0])

    def test_next_step(self):
        f = Intcode()
        self.assertEqual(([1002, 4, 3, 4, 99], 4, [], []), f.next_step([1002, 4, 3, 4, 33], 0, [], []))
        self.assertEqual(([1101, 100, -1, 4, 99], 4, [], []), f.next_step([1101, 100, -1, 4, 0], 0, [], []))
        self.assertEqual(([4, 2, -1], 2, [], [-1]), f.next_step([4, 2, -1], 0, [], []))
        self.assertEqual(([3, 2, 5], 2, [], []), f.next_step([3, 2, -1], 0, [5], []))
        self.assertEqual(([2, 0, 0, 0, 99], 4, [], []), f.next_step([1, 0, 0, 0, 99], 0, [], []))
        self.assertEqual(([2, 3, 0, 6, 99], 4, [], []), f.next_step([2, 3, 0, 3, 99], 0, [], []))
        self.assertEqual(([2, 4, 4, 5, 99, 9801], 4, [], []), f.next_step([2, 4, 4, 5, 99, 0], 0, [], []))
        self.assertEqual(([1, 1, 1, 4, 2, 5, 6, 0, 99], 4, [], []), f.next_step([1, 1, 1, 4, 99, 5, 6, 0, 99], 0, [], []))
        self.assertEqual(([30, 1, 1, 4, 2, 5, 6, 0, 99], 8, [], []), f.next_step([1, 1, 1, 4, 2, 5, 6, 0, 99], 4, [], []))



#unittest.main()

intcode = Intcode()
code_ = list(map(int, "3,8,1001,8,10,8,105,1,0,0,21,34,43,64,85,98,179,260,341,422,99999,3,9,1001,9,3,9,102,3,9,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,1001,9,2,9,1002,9,4,9,1001,9,3,9,1002,9,4,9,4,9,99,3,9,1001,9,3,9,102,3,9,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,1002,9,3,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99".split(",")))
print(intcode.max_phase_parallel(code_))
