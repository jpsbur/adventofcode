import unittest
import itertools

class State:

    def __init__(self, code, ip=0, rb=0, fin=[], fout=[]):
        if isinstance(code, dict):
            self.code = code[:]
        else:
            self.code = {i: code[i] for i in range(len(code))}
        self.ip = ip
        self.rb = rb
        self.fin = fin[:]
        self.fout = fout[:]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def get_operation(self):
        return self.get_code(self.ip) % 100

    def get_mode(self, ind):
        mask = self.get_code(self.ip) // 100
        return (mask // (10 ** ind)) % 10

    def get_pos(self, ind):
        return self.ip + 1 + ind

    def get_code(self, pos):
        if pos not in self.code:
            self.code[pos] = 0
        return self.code[pos]

    def set_code(self, pos, val):
        self.code[pos] = val

    def get_operand(self, ind):
        pos = self.get_pos(ind)
        mode = self.get_mode(ind)
        if mode == 0:
            return self.get_code(self.get_code(pos))
        elif mode == 1:
            return self.get_code(pos)
        elif mode == 2:
            return self.get_code(self.get_code(pos) + self.get_rb())
        else:
            assert False

    def set_operand(self, ind, val):
        pos = self.get_pos(ind)
        mode = self.get_mode(ind)
        if mode == 0:
            self.set_code(self.get_code(pos), val)
        elif mode == 2:
            self.set_code(self.get_code(pos) + self.get_rb(), val)
        else:
            assert False

    def read(self):
        res = self.fin[0]
        self.fin = self.fin[1:]
        return res

    def write(self, val):
        self.fout.append(val)

    def append_to_read_buffer(self, val):
        self.fin += val

    def flush_write_buffer(self):
        res = self.fout[:]
        self.fout = []
        return res

    def inc_ip(self, val):
        self.ip += val

    def set_ip(self, val):
        self.ip = val

    def get_rb(self):
        return self.rb

    def inc_rb(self, val):
        self.rb += val

    def is_terminated(self):
        return self.get_operation() == 99

    def is_blocked_on_input(self):
        return self.get_operation() == 3 and len(self.fin) == 0

    def next_step(self):
        rop = self.get_operation()
        if rop == 99:
            pass
        if rop == 1:
            a = self.get_operand(0)
            b = self.get_operand(1)
            self.set_operand(2, a + b)
            self.inc_ip(4)
        elif rop == 2:
            a = self.get_operand(0)
            b = self.get_operand(1)
            self.set_operand(2, a * b)
            self.inc_ip(4)
        elif rop == 3:
            self.set_operand(0, self.read())
            self.inc_ip(2)
        elif rop == 4:
            self.write(self.get_operand(0))
            self.inc_ip(2)
        elif rop == 5:
            a = self.get_operand(0)
            b = self.get_operand(1)
            if a != 0:
                self.set_ip(b)
            else:
                self.inc_ip(3)
        elif rop == 6:
            a = self.get_operand(0)
            b = self.get_operand(1)
            if a == 0:
                self.set_ip(b)
            else:
                self.inc_ip(3)
        elif rop == 7:
            a = self.get_operand(0)
            b = self.get_operand(1)
            if a < b:
                self.set_operand(2, 1)
            else:
                self.set_operand(2, 0)
            self.inc_ip(4)
        elif rop == 8:
            a = self.get_operand(0)
            b = self.get_operand(1)
            if a == b:
                self.set_operand(2, 1)
            else:
                self.set_operand(2, 0)
            self.inc_ip(4)
        elif rop == 9:
            self.inc_rb(self.get_operand(0))
            self.inc_ip(2)
        return self



class Intcode:

    def run(self, code_, fin_):
        state = State(code_, fin=fin_)
        while state.get_operation() != 99:
            state.next_step()
        return state.fout

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
        n = len(codes_)
        inps = inps_[:]
        inps[0].append(0)
        states = [State(codes_[i], fin=inps[i]) for i in range(n)]
        while True:
            any_step = False
            for i in range(n):
                if states[i].is_terminated():
                    continue
                if states[i].is_blocked_on_input():
                    continue
                states[i].next_step()
                states[(i + 1) % n].append_to_read_buffer(states[i].flush_write_buffer())
                any_step = True
                break
            if not any_step:
                break
        return states[0].fin

    def max_phase_parallel(self, code):
        best = None
        for p in list(itertools.permutations([5, 6, 7, 8, 9])):
            x = self.run_parallel([code[:] for _ in range(5)], [[a] for a in p])[0]
            if best is None or x > best:
                best = x
        return best


class TestIntcodeParallel(unittest.TestCase):

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


class TestIntcodeMax(unittest.TestCase):

    def test_max_phase(self):
        f = Intcode()
        code = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
        self.assertEqual(43210, f.max_phase(code))
        code = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
        self.assertEqual(54321, f.max_phase(code))
        code = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
        self.assertEqual(65210, f.max_phase(code))


class TestIntcodeRun(unittest.TestCase):

    def test_run_uninitialized_memory(self):
        f = Intcode()
        code = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
        self.assertEqual(code, f.run(code, []))

    def test_run_large_numbers(self):
        f = Intcode()
        code = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
        self.assertEqual([1219070632396864], f.run(code, []))
        code = [104, 1125899906842624, 99]
        self.assertEqual([1125899906842624], f.run(code, []))

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


class TestState(unittest.TestCase):

    def test_next_step(self):
        self.assertEqual(
            State([109, 19, 204, -2019, 99], ip=4, rb=2019, fout=[109]),
            State([109, 19, 204, -2019, 99], ip=2, rb=2019).next_step())
        self.assertEqual(
            State([109, 19, 99], ip=2, rb=2019),
            State([109, 19, 99], rb=2000).next_step())
        self.assertEqual(
            State([1002, 4, 3, 4, 99], ip=4),
            State([1002, 4, 3, 4, 33]).next_step())
        self.assertEqual(
            State([1101, 100, -1, 4, 99], ip=4),
            State([1101, 100, -1, 4, 0]).next_step())
        self.assertEqual(
            State([4, 2, -1], ip=2, fout=[-1]),
            State([4, 2, -1]).next_step())
        self.assertEqual(
            State([3, 2, 5], ip=2),
            State([3, 2, -1], fin=[5]).next_step())
        self.assertEqual(
            State([2, 0, 0, 0, 99], ip=4),
            State([1, 0, 0, 0, 99]).next_step())
        self.assertEqual(
            State([2, 3, 0, 6, 99], ip=4),
            State([2, 3, 0, 3, 99]).next_step())
        self.assertEqual(
            State([2, 4, 4, 5, 99, 9801], ip=4),
            State([2, 4, 4, 5, 99, 0]).next_step())
        self.assertEqual(
            State([1, 1, 1, 4, 2, 5, 6, 0, 99], ip=4),
            State([1, 1, 1, 4, 99, 5, 6, 0, 99]).next_step())
        self.assertEqual(
            State([30, 1, 1, 4, 2, 5, 6, 0, 99], ip=8),
            State([1, 1, 1, 4, 2, 5, 6, 0, 99], ip=4).next_step())



#unittest.main()

intcode = Intcode()
code = list(map(int, "1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,902,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,309,0,1024,1101,0,24,1002,1102,388,1,1029,1102,1,21,1019,1101,0,33,1015,1102,1,304,1025,1101,344,0,1027,1101,25,0,1003,1102,1,1,1021,1101,29,0,1012,1101,0,23,1005,1102,1,32,1007,1102,38,1,1000,1101,30,0,1016,1102,1,347,1026,1101,0,26,1010,1101,0,39,1004,1102,1,36,1011,1101,0,393,1028,1101,0,37,1013,1101,0,35,1008,1101,34,0,1001,1101,0,495,1022,1102,1,28,1018,1101,0,0,1020,1102,1,22,1006,1101,488,0,1023,1102,31,1,1009,1102,1,20,1017,1101,0,27,1014,109,10,21102,40,1,4,1008,1014,37,63,1005,63,205,1001,64,1,64,1106,0,207,4,187,1002,64,2,64,109,-18,1207,8,37,63,1005,63,227,1001,64,1,64,1106,0,229,4,213,1002,64,2,64,109,17,1207,-7,25,63,1005,63,247,4,235,1106,0,251,1001,64,1,64,1002,64,2,64,109,-8,1202,6,1,63,1008,63,29,63,1005,63,275,1001,64,1,64,1106,0,277,4,257,1002,64,2,64,109,25,1205,-6,293,1001,64,1,64,1105,1,295,4,283,1002,64,2,64,109,-4,2105,1,2,4,301,1106,0,313,1001,64,1,64,1002,64,2,64,109,-9,1208,-4,31,63,1005,63,335,4,319,1001,64,1,64,1105,1,335,1002,64,2,64,109,16,2106,0,-2,1106,0,353,4,341,1001,64,1,64,1002,64,2,64,109,-13,2102,1,-8,63,1008,63,38,63,1005,63,373,1105,1,379,4,359,1001,64,1,64,1002,64,2,64,109,9,2106,0,3,4,385,1105,1,397,1001,64,1,64,1002,64,2,64,109,-11,21107,41,42,0,1005,1014,415,4,403,1106,0,419,1001,64,1,64,1002,64,2,64,109,14,1206,-7,431,1106,0,437,4,425,1001,64,1,64,1002,64,2,64,109,-23,2107,37,-5,63,1005,63,455,4,443,1105,1,459,1001,64,1,64,1002,64,2,64,109,10,21107,42,41,-2,1005,1013,475,1105,1,481,4,465,1001,64,1,64,1002,64,2,64,2105,1,8,1001,64,1,64,1106,0,497,4,485,1002,64,2,64,109,-6,21108,43,41,8,1005,1017,517,1001,64,1,64,1106,0,519,4,503,1002,64,2,64,109,5,2101,0,-9,63,1008,63,23,63,1005,63,541,4,525,1106,0,545,1001,64,1,64,1002,64,2,64,109,-13,1201,5,0,63,1008,63,20,63,1005,63,565,1105,1,571,4,551,1001,64,1,64,1002,64,2,64,109,16,1205,4,589,4,577,1001,64,1,64,1106,0,589,1002,64,2,64,109,-16,1202,4,1,63,1008,63,23,63,1005,63,615,4,595,1001,64,1,64,1106,0,615,1002,64,2,64,109,1,2101,0,6,63,1008,63,33,63,1005,63,639,1001,64,1,64,1105,1,641,4,621,1002,64,2,64,109,8,21101,44,0,8,1008,1018,44,63,1005,63,667,4,647,1001,64,1,64,1105,1,667,1002,64,2,64,109,-7,1201,1,0,63,1008,63,39,63,1005,63,689,4,673,1106,0,693,1001,64,1,64,1002,64,2,64,109,7,2102,1,-8,63,1008,63,24,63,1005,63,715,4,699,1105,1,719,1001,64,1,64,1002,64,2,64,109,5,2108,34,-7,63,1005,63,739,1001,64,1,64,1105,1,741,4,725,1002,64,2,64,109,-22,2108,25,10,63,1005,63,763,4,747,1001,64,1,64,1106,0,763,1002,64,2,64,109,31,1206,-4,781,4,769,1001,64,1,64,1105,1,781,1002,64,2,64,109,-10,21101,45,0,5,1008,1019,47,63,1005,63,805,1001,64,1,64,1105,1,807,4,787,1002,64,2,64,109,2,21108,46,46,-3,1005,1013,825,4,813,1106,0,829,1001,64,1,64,1002,64,2,64,109,-22,2107,40,10,63,1005,63,845,1105,1,851,4,835,1001,64,1,64,1002,64,2,64,109,17,1208,-7,36,63,1005,63,871,1001,64,1,64,1105,1,873,4,857,1002,64,2,64,109,16,21102,47,1,-9,1008,1018,47,63,1005,63,899,4,879,1001,64,1,64,1106,0,899,4,64,99,21102,1,27,1,21101,0,913,0,1105,1,920,21201,1,39657,1,204,1,99,109,3,1207,-2,3,63,1005,63,962,21201,-2,-1,1,21102,1,940,0,1105,1,920,21201,1,0,-1,21201,-2,-3,1,21101,955,0,0,1105,1,920,22201,1,-1,-2,1106,0,966,21202,-2,1,-2,109,-3,2105,1,0".split(",")))
print(intcode.run(code, [1]))
print(intcode.run(code, [2]))
