import unittest

class Intcode:

    def next_step(self, code_, i):
        code = code_[:]
        op = code[i]
        if op == 99:
            return code
        a = code[code[i + 1]]
        b = code[code[i + 2]]
        if op == 1:
            code[code[i + 3]] = a + b
        elif op == 2:
            code[code[i + 3]] = a * b
        return code

    def run(self, code_):
        code = code_[:]
        pos = 0
        while code[pos] != 99:
            code = intcode.next_step(code, pos)
            pos += 4
        return code[0]


class TestIntcode(unittest.TestCase):

    def test_next_step(self):
        f = Intcode()
        self.assertEqual([2, 0, 0, 0, 99], f.next_step([1, 0, 0, 0, 99], 0))
        self.assertEqual([2, 3, 0, 6, 99], f.next_step([2, 3, 0, 3, 99], 0))
        self.assertEqual([2, 4, 4, 5, 99, 9801], f.next_step([2, 4, 4, 5, 99, 0], 0))
        self.assertEqual([1, 1, 1, 4, 2, 5, 6, 0, 99], f.next_step([1, 1, 1, 4, 99, 5, 6, 0, 99], 0))
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], f.next_step([1, 1, 1, 4, 2, 5, 6, 0, 99], 4))



#unittest.main()

intcode = Intcode()
code_ = list(map(int, input().split(',')))
for noun in range(100):
    for verb in range(100):
        code = code_[:]
        code[1] = noun
        code[2] = verb
        x = intcode.run(code)
        if x == 19690720:
            print([noun, verb, 100 * noun + verb])
